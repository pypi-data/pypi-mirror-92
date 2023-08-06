"""
Probabilistic model
"""
from collections import defaultdict
from .scan import MultiShell, Shell
import numpy as np
from mcot.maths import spherical
from scipy import optimize, spatial
from .simulator import random_eddy_params, FibrePopulation
from copy import deepcopy
import xarray
from typing import Sequence, Union
import sympy as sym
from functools import lru_cache


def default_dependencies():
    """
    Defines which parameters depend on which variables

    :return: a ("param"x"depends") boolean xarray, which is True if a specific parameter varies along a specific axis
        (e.g., log_g depends on fibre population, but not any of the acquisition parameters, so is only true for depends=fibre)
    """
    all_params = ['theta', 'phi', 'width', 'dphase', 'log_g', 'f_myelin', 'log_g_myelin', 'non_myelin',
                  'amplitude_se', 'R2_attenuation', 'R2', 'R2i', 'eddy_odd', 'eddy_even']
    return xarray.DataArray(
        [
           # fibre, bval, b0_group, t_phase
            [True, False, False, False],  # theta
            [True, False, False, False],  # phi
            [True, True, False, False],   # width
            [True, True, True, True],    # dphase
            [True, True, False, False],   # log_g
            [True, True, False, False],   # f_myelin
            [True, False, False, False],  # log_g_myelin
            [False, True, True, False],   # non_myelin
            [True, True, False, False],   # amplitude_se
            [False, False, True, True],   # R2_attenuation
            [True, False, True, False],   # R2
            [True, False, True, False],   # R2i
            [False, True, True, True],    # eddy_odd
            [False, True, True, False],   # eddy_even
        ],
        coords=[
            ('param', all_params),
            ('depends', ['fibre', 'bval', 'b0_group', 't_phase']),
        ]
    )


class Parameters:
    """
    Object representing a set of model parameters across all shells and fibre populations (for a single voxel)

    All parameters:
    - `orient` Bingham distribution orientation
    - `width` width of Bingham distribution
    - `log_g` average log(g). Only used for single-population model
    - `f_myelin` fraction of myelinated axons. Only used for two-population model
    - `log_g_myelin` log g-ratio of myelinated axons. Only used for two-population model
    - `non_myelin` off-resonance frequency due to non-myelin sources
    - `movement_phase` random phase offset due to movement
    - `amplitude_se` amplitude of the signal parallel to the fibres at the first spin echo readout
    - `amplitude_ase` amplitude of the signal parallel to the fibres at the second asymmetric spin echo readout
    - `R2` irreversible rate of transverse signal decay (inverse of T2)
    - `R2i` reversible rate of transverse signal decay (R2 + R2i is the inverse of T2*)
    - `eddy_odd` odd components of the eddy currents
    - `eddy_even` even components of the eddy currents
    """
    def __init__(self, as_dict: dict, shells: Union[MultiShell, Sequence[Shell]], eddy_lmax: int):
        """
        Creates a new parameter set based on provided dictionary

        :param as_dict: maps parameters name to a tuple with:

            - (N, ) index array for N shells, where each shell is mapped to M parameters (with M<= N)
            - (M, ) jax array with the parameter values

        :param shells: (N, ) sequence of shells defining how the data was acquired
        :param eddy_lmax: maximum degree of the spherical harmonic fit to the eddy components (odd or even)
        """
        self.as_dict = as_dict
        if not isinstance(shells, MultiShell):
            shells = MultiShell(shells)
        self.shells = shells
        self.eddy_lmax = eddy_lmax

    @classmethod
    def empty(cls, shells: Union[MultiShell, Sequence[Shell]], nfibres=2, eddy_lmax=1, dependencies=None):
        """
        Defines for each parameter on which level they will vary.

        :param shells: sequence of shells defining how the data was acquired
        :param nfibres: number of crossing fibres
        :param eddy_lmax: maximum order of the spherical harmonics used to fit the eddy currents
        :param dependencies: on what observatinal variables does each parameter depend
            (defaults to result of :func:`default_dependencies`)
        """
        if not isinstance(shells, MultiShell):
            shells = MultiShell(shells)
        if dependencies is None:
            dependencies = default_dependencies()
        if eddy_lmax > 0:
            neddy_odd = shells[0].spherical_harmonics(eddy_lmax, odd=True).shape[-1]
            neddy_even = shells[0].spherical_harmonics(eddy_lmax, odd=False).shape[-1]
        else:
            neddy_odd, neddy_even = 0, 0

        as_dict = {}
        for name, default in [
            ('theta', 0),
            ('phi', 0),
            ('width', 1.),
            ('dphase', 0.),
            ('log_g', 0.5 * np.log(0.7)),
            ('f_myelin', 0.5),
            ('log_g_myelin', np.log(0.7)),
            ('non_myelin', 0.),
            ('amplitude_se', 1.),
            ('R2_attenuation', 0.5),
            ('R2', 0.002),
            ('R2i', 0.002),
            ('eddy_odd', np.zeros(neddy_odd)),
            ('eddy_even', np.zeros(neddy_even)),
        ]:
            depends_on = dependencies.sel(param=name).values
            shell_indices = []
            all_indices = []
            for indices, shell in shells.enumerated():
                use_indices = [index for index, valid in zip(indices, depends_on[1:]) if valid]
                if not use_indices in all_indices:
                    all_indices.append(use_indices)
                shell_indices.append(all_indices.index(use_indices))
            values = [np.array(default) if not depends_on[0] else [np.array(default) for _ in range(nfibres)]
                      for _ in all_indices]
            as_dict[name] = (shell_indices, values)

        as_dict['movement_phase'] = (list(range(len(shells))), [
            np.zeros(shell.ngradients) for shell in shells.shells
        ])

        return cls(as_dict, shells, eddy_lmax)

    def guess_orient(self, all_data):
        """
        Guesses the fibre orientation fits and updates them in place

        Guesses are based on diffusion tensor fit to the the spin echo data for the first shell

        First fibre is updated to point in direction of V1
        Second fibre is updated to point in direction of V2
        Third fibre is updated to point in direction of V3
        """
        shell, shell_params = next((p for p in self))
        data = abs(all_data[0][0])  # spin echo data for first shell
        lines = []
        for dim in range(3):
            lines.append(shell.gradients[:, dim] ** 2)
            for dim2 in range(dim):
                lines.append(2 * shell.gradients[:, dim] * shell.gradients[:, dim2])
        ldata = -np.log(data) / shell.bval
        params = np.linalg.lstsq(np.stack(lines, -1), ldata, rcond=None)[0]

        tensor = np.zeros((3, 3))
        idx = 0
        for dim in range(3):
            tensor[dim, dim] = params[idx]
            idx += 1
            for dim2 in range(dim):
                tensor[dim, dim2] = params[idx]
                tensor[dim2, dim] = params[idx]
                idx += 1
        vals, vecs = np.linalg.eigh(tensor)
        for idx_fibre in range(self.nfibres):
            _, phi, theta = spherical.cart2spherical(*vecs[:, -idx_fibre-1])
            for fibre_list in self.as_dict['theta'][1]:
                fibre_list[idx_fibre] = np.array(theta)
            for fibre_list in self.as_dict['phi'][1]:
                fibre_list[idx_fibre] = np.array(phi)

    @property
    def nfibres(self, ):
        """
        Number of fibre populations estimated
        """
        return len(self.as_dict['phi'][1][0])

    def __iter__(self, ):
        """
        Iterate over all shells, yielding for each shell a tuple with:

            - the shell
            - list of dictionary-like objects with the parameters for each fibre population
        """
        for idx, shell in enumerate(self.shells.shells):
            yield shell, [ShellParams(self, idx_fibre, idx) for idx_fibre in range(self.nfibres)]

    def random_confounds(self, shot_phase=True, eddy_odd=True, eddy_even=False, non_myelin=True):
        """
        Randomly set any of the confounds that are set to True

        :param shot_phase: assign each shot a random phase between 0 and 2 pi
        :param eddy_odd: odd components of the eddy current spherical harmonics
        :param eddy_even: even components of the eddy current spherical harmonics
        :param non_myelin: susceptibility from non-myelin sources
        """
        params_odd = {}
        params_even = {}
        for shell, param_list in self:
            if eddy_odd and shell.bval not in params_odd:
                params_odd[shell.bval] = random_eddy_params(self.eddy_lmax, odd=True)
            if eddy_even and shell.bval not in params_even:
                params_even[shell.bval] = random_eddy_params(self.eddy_lmax, odd=False)
            for params in param_list:
                if shot_phase:
                    params['movement_phase'] = np.random.rand(shell.ngradients) * 2 * np.pi
                if eddy_odd:
                    p = params_odd[shell.bval]
                    params['eddy_odd'] = p[:, 0] + p[:, 1] * shell.t_phase
                if eddy_even:
                    p = params_even[shell.bval]
                    params['eddy_even'] = p[:, 0] + p[:, 1] * shell.t_phase
                if non_myelin:
                    params['non_myelin'] = np.random.randn() * 20

    def set_population(self, index, population: FibrePopulation):
        """
        Sets the magnitude and log(g) based on the fibre population

        :param index: which crossing fibre to set (0-based)
        :param population: object describing a fibre population
        """
        for shell, param_list in self:
            param = param_list[index]
            param['theta'] = population.theta
            param['phi'] = population.phi
            param['width'] = population.d_parallel - population.d_perpendicular
            first_echo = (
                    population.M0 *
                    np.exp(-shell.bval * population.d_perpendicular) *
                    np.exp(-shell.readout1 / population.T2)
            )
            param['amplitude_se'] = first_echo
            second_ro = (
                    first_echo *
                    np.exp(-(shell.readout2 - shell.readout1) / population.T2) *
                    np.exp(-shell.t_phase / population.T2i)
            )
            param['R2_attenuation'] = second_ro / first_echo
            param['R2'] = 1/population.T2
            param['R2i'] = 1/population.T2i
            param['f_myelin'] = population.f_myelin
            param['log_g_myelin'] = np.log(population.g_ratio)
            param['log_g'] = population.f_myelin * np.log(population.g_ratio)

    def to_change(self, tofit):
        """
        Returns sequence of arrays that should be changed during fitting

        :param tofit: name of the parameters to fit
        :return: tuple with

            - (N, ) list of arrays
            - dictionary mapping (parameter name, idx_shell, idx_fibre) to corresponding index in the returned array
        """
        arrs = []
        mapping = {}
        for name in tofit:
            diff_fibre = isinstance(self.as_dict[name][1][0], list)
            for idx_shell, idx_arr in enumerate(self.as_dict[name][0]):
                idx_start = len(arrs) + idx_arr * (self.nfibres if diff_fibre else 1)
                for idx_fibre in range(self.nfibres):
                    mapping[(name, idx_shell, idx_fibre)] = idx_start + idx_fibre * diff_fibre
            if diff_fibre:
                for fibre_arrs in self.as_dict[name][1]:
                    arrs.extend(fibre_arrs)
            else:
                arrs.extend(self.as_dict[name][1])
        return arrs, mapping

    def to_dict(self, ):
        """
        Converts object into a dictionary
        """
        return {
            'eddy_lmax': self.eddy_lmax,
            'shells': self.shells.to_list(),
            'parameters': self.as_dict
        }

    @classmethod
    def from_dict(cls, a_dict):
        """
        Converts dictionary back into Parameters object
        """
        return cls(
            a_dict['parameters'],
            MultiShell.from_list(a_dict['shells']),
            a_dict['eddy_lmax'],
        )

    def copy(self):
        """
        Copies the object

        :return: new Parameter object with a deep copy of the actual parameters, but shallow copy of the shells
        """
        return Parameters(
            deepcopy(self.as_dict),
            self.shells,
            self.eddy_lmax
        )

    def to_xarray(self, ):
        """
        Converts all parameters (excluding movement_phase) to an xarray object for later analysis
        """
        as_dict = defaultdict(list)
        for idx_shell, (shell, params) in enumerate(self):
            for name in self.as_dict.keys():
                if name != 'movement_phase':
                    vals = [p[name][0] if p[name].shape == (1, ) else p[name] for p in params]
                    as_dict[name].append(vals)
        second_dim = {'eddy_odd': ('m_odd', ), 'eddy_even': ('m_even', )}
        res = {name: xarray.DataArray(
            arr, coords={'shell': self.shells.coords1d},
            dims=('shell', 'fibre') + second_dim.get(name, ())) for name, arr in as_dict.items()}
        return xarray.Dataset(res, attrs={'eddy_lmax': self.eddy_lmax})


class ShellParams:
    """
    Dictionary-like object to read/write parameters for a single shell of diffusion-weighted phase data
    """
    def __init__(self, all_params: Parameters, idx_fibre, idx_shell):
        """
        Creates interface to parameters for given shell and fibre population

        :param all_params: object with all parameters across shells and fibre populations
        :param idx_fibre: index of fibre population
        :param idx_shell: index of shell
        """
        self.all_params = all_params
        self.idx_fibre = idx_fibre
        self.idx_shell = idx_shell

    def __getitem__(self, name):
        """
        Reads one of the parameters for the appropriate shell/fibre population

        :param name: parameter name
        :return: jax array with the parameters
        """
        indices, params = self.all_params.as_dict[name]
        param = params[indices[self.idx_shell]]
        if isinstance(param, list):
            return param[self.idx_fibre]
        return param

    def __setitem__(self, name, value):
        """
        Sets one of the parameters to a new value for the appropriate shell/fibre population

        The value is converted into a jax array before storing

        :param name: parameter name
        :param value: new value
        """
        indices, params = self.all_params.as_dict[name]
        param = params[indices[self.idx_shell]]
        if isinstance(param, list):
            param[self.idx_fibre] = np.array(value)
        else:
            params[indices[self.idx_shell]] = np.array(value)

    def __iter__(self, ):
        """
        iterate over all parameter names
        """
        yield from self.all_params.as_dict.keys()

    def items(self, ):
        for key in self:
            yield (key, self[key])


class Model(object):
    """
    Model to fit to the DIPPI data
    """
    def __init__(self, shells: MultiShell, T2=False, dual_phase=False, only_phase=False):
        """
        Creates a new DIPPI model

        :param shells: Describes the acquisition parameters
        :param T2: if True fit R2 and R2* instead of fitting each amplitude independently
        :param dual_phase: if True fit unmyelinated and myelinated axons as separate compartments
        :param only_phase: Ignore the biophysical model and just fit the phase difference between readouts for every dyad
        """
        self.shells = shells
        self.T2 = T2
        if dual_phase and only_phase:
            raise ValueError("dual_phase and only_phase are conflicting model definitions")
        self.dual_phase = dual_phase
        self.only_phase = only_phase

        amplitude_se, R2_attenuation, R2, R2i, width, theta, phi = sym.symbols(
            'amplitude_se, R2_attenuation, R2, R2i, width, theta, phi'
        )
        movement_phase, eddy_phase, non_myelin, log_g, log_g_myelin, f_myelin, dphase = sym.symbols(
            'movement_phase, eddy_phase, non_myelin, log_g, log_g_myelin, f_myelin, dphase'
        )
        bvec = sym.symbols('bvec:3')

        self.magnitude_equations = []
        self.signal_equations = []
        for shell in self.shells:
            profile = sym.exp(-shell.bval * width * alignment(phi, theta, bvec) ** 2)
            magnitude_se = amplitude_se * profile
            if T2:
                R2_attenuation = sym.exp(-(shell.readout2 - shell.readout1) * R2 - shell.t_phase * R2i)
            magnitude_ase = R2_attenuation * amplitude_se * profile
            self.magnitude_equations.append((magnitude_se, magnitude_ase))

            signal_se = magnitude_se * sym.exp(1j * movement_phase)

            confound_phase = movement_phase + (non_myelin * shell.t_phase) + eddy_phase
            if dual_phase:
                angle = myelin_phase(shell, phi, theta, log_g_myelin)
                norm_myelin = sym.sqrt(((1 - f_myelin) + f_myelin * sym.cos(angle)) ** 2 + (f_myelin * sym.sin(angle)) ** 2)
                myelin_part = (
                    f_myelin * sym.exp(1j * angle) +
                    (1 - f_myelin)
                ) / norm_myelin
                signal_ase = magnitude_ase * sym.exp(1j * confound_phase) * myelin_part
            elif only_phase:
                signal_ase = magnitude_ase * sym.exp(1j * (movement_phase + dphase + eddy_phase))
            else:
                signal_ase = magnitude_ase * sym.exp(
                    1j * (confound_phase + myelin_phase(shell, phi, theta, log_g))
                )
            self.signal_equations.append((signal_se, signal_ase))

        self.parameter_names = tuple(sorted(str(v) for v in signal_ase.free_symbols.union(signal_se.free_symbols)))

    def derivative(self, name):
        """
        Computes the derivative with respect to a given parameter

        This function uses cacheing

        :param name: name of one of the parameters
        :return: sympy equations with derivative as a list with the equation for each shell and both readouts
        """
        return [[sym.diff(f, name) for f in fs] for fs in self.signal_equations]

    def funcs(self, derivative=None, only_mag=False):
        """
        Return the model equations as numpy functions

        :param derivative: set to a name to return the derivative with respect to that parameter
        :param only_mag: if True only compute the magnitude rather than the complex signal
        :return: for each shell return a tuple with functions for the first and second readout signal (or its derivatives)
        """
        equations = self.magnitude_equations if only_mag else self.signal_equations
        return [tuple(_lambdify_equation_cached(self.parameter_names, readout, derivative) for readout in shell)
                for shell in equations]

    def func_args(self, parameters: Parameters, to_vary=()):
        """
        Fills in the arguments for the numpy functions from self.:meth:`funcs`

        :param parameters: current best estimate of the parameters
        :param to_vary: names of the parameters that should not be filled in yet (None placeholder)
        :return: for each shell a list of arguments (which are the same for the first and second readout)
        """
        res = []
        for shell, sparams in parameters:
            res.append([])
            for param in sparams:
                res[-1].append([])
                eddy_phase = np.zeros(shell.ngradients)
                if parameters.eddy_lmax > 0:
                    if 'eddy_odd' not in to_vary:
                        eddy_phase += shell.spherical_harmonics(parameters.eddy_lmax, odd=True).dot(param['eddy_odd'])
                    if 'eddy_even' not in to_vary:
                        eddy_phase += shell.spherical_harmonics(parameters.eddy_lmax, odd=False).dot(param['eddy_even'])
                for name in self.parameter_names:
                    if name == 'eddy_phase':
                        value = eddy_phase
                    elif name.startswith('bvec'):
                        idx = int(name[-1])
                        value = shell.gradients[:, idx]
                    elif name in to_vary:
                        value = None
                    else:
                        value = param[name]

                    res[-1][-1].append(value)
        return res

    def signal(self, parameters: Parameters, only_mag=False, split_fibres=False):
        """
        Computes the signal given a set of parameters

        :param parameters: set of model parameters
        :param only_mag: if True return the magnitude rather than the complex signal
        :param split_fibres: if True return the signal for each fibre population individually
        :return: a list with for each shell the signal during the first and second readout
        """
        res = []
        for shell, all_params, all_funcs in zip(parameters.shells, self.func_args(parameters), self.funcs(only_mag=only_mag)):
            res.append([])
            for readout_func in all_funcs:
                if split_fibres:
                    res[-1].append([])
                else:
                    res[-1].append(np.zeros(shell.ngradients, dtype=float if only_mag else complex))
                for fibre_param in all_params:
                    if split_fibres:
                        res[-1][-1].append(readout_func(*fibre_param))
                    else:
                        res[-1][-1] += readout_func(*fibre_param)
        return res

    def cost(self, parameters: Parameters, data, only_mag=False):
        """
        Squared offset between the model signal and observed data

        :param parameters: set of model parameters
        :param data: input data (list with for each shell the complex signal during first and second readout)
        :param only_mag: if True only consider the magnitude rather than the complex signal
        :return: total cost across all shells and readouts
        """
        signal = self.signal(parameters, only_mag=only_mag)
        ct = 0.
        for model, observed in zip(signal, data):
            for m, o in zip(model, observed):
                if only_mag:
                    ct += np.sum((m - abs(o)) ** 2)
                else:
                    ct += np.sum(abs(m - o) ** 2)
        return ct

    def get_cost(self, parameters: Parameters, data, tofit, only_mag=False):
        """
        Returns a set of functions that allows for efficient evalution of the model during model optimisation

        Used internally by :func:`singla_fit` and `model_fit`.

        :param parameters: initial set of parameters
        :param data: input data (list with for each shell the complex signal during first and second readout)
        :param tofit: sequence with parameter names to fit
        :param only_mag: if True only fit the mangitude rather than the complex signal
        :return: A tuple with:

            - function that given an array with current parameter values returns the cost and its derivatives
            - function that turns array of best-fit parameter values back into a Parameter object
            - array with initial parameter values
        """
        all_functions = self.funcs(only_mag=only_mag)
        all_derivatives = {name: self.funcs(name, only_mag=only_mag) for name in tofit}
        if 'eddy_odd' in tofit or 'eddy_even' in tofit:
            all_derivatives['eddy_phase'] = self.funcs('eddy_phase', only_mag=only_mag)
        array_params = self.func_args(parameters, to_vary=tofit)
        struct_params = parameters.copy()
        to_change, map_derivative = struct_params.to_change(tofit)
        init = np.concatenate([[]] + [a.flatten() for a in to_change])

        idx = 0
        edges = [0]
        for arr in to_change:
            idx += arr.size
            edges.append(idx)

        def write_struct_params(new_params):
            """
            Updates reference Parameters object with new values

            :param new_params: new guess for values of fitted parameters in array form
            """
            idx = 0
            for arr in to_change:
                arr[()] = new_params[idx:idx+arr.size].reshape(arr.shape)
                idx += arr.size

        def convert_params(new_params):
            """
            Converts set of parameters in array form into new Parameter object

            :param new_params: best-fit values for the fitted parameters
            :return: new object containing all the parameter values (both fixed and fitted)
            """
            write_struct_params(new_params)
            return struct_params.copy()

        def cost(new_params):
            """
            Computes the cost and its derivative

            :param new_params: new guess for values of fitted parameters in array form
            :return: float with cost and array with Jacobian
            """
            new_params = np.asanyarray(new_params)
            write_struct_params(new_params)

            ct = 0.
            dp = np.zeros(new_params.size)
            for idx_shell, (shell, sparams) in enumerate(struct_params):
                if struct_params.eddy_lmax > 0:
                    if 'eddy_odd' in tofit:
                        mat_eddy_odd = shell.spherical_harmonics(struct_params.eddy_lmax, odd=True)
                    if 'eddy_even' in tofit:
                        mat_eddy_even = shell.spherical_harmonics(struct_params.eddy_lmax, odd=False)
                else:
                    mat_eddy_odd = np.zeros((shell.ngradients, 0))
                    mat_eddy_even = mat_eddy_odd
                fibre_params = []
                for idx_fibre in range(struct_params.nfibres):
                    param_array = list(array_params[idx_shell][idx_fibre])
                    for name in tofit:
                        if name.startswith('eddy_'):
                            idx = self.parameter_names.index('eddy_phase')
                            mat = mat_eddy_odd if name == 'eddy_odd' else mat_eddy_even
                            param_array[idx] = param_array[idx] + mat.dot(sparams[idx_fibre][name])
                        else:
                            idx = self.parameter_names.index(name)
                            param_array[idx] = sparams[idx_fibre][name]
                    fibre_params.append(param_array)

                for idx_readout in range(2):
                    signal = np.zeros(shell.ngradients, dtype=float if only_mag else complex)
                    for param_array in fibre_params:
                        signal += all_functions[idx_shell][idx_readout](*param_array)
                    observed = data[idx_shell][idx_readout]
                    if only_mag or not np.iscomplex(observed).any():
                        ct_part = ((np.real(signal) - abs(observed)) ** 2).sum()
                        der_signal = 2 * (np.real(signal) - abs(observed))
                    else:
                        ct_part = (abs(signal - observed) ** 2).sum()
                        der_signal = np.conj(2 * (signal - observed))
                    ct += ct_part

                    for idx_fibre, param_array in enumerate(fibre_params):
                        if 'eddy_odd' in tofit or 'eddy_even' in tofit:
                            dphase = all_derivatives['eddy_phase'][idx_shell][idx_readout](*param_array) * der_signal
                        for name in tofit:
                            if name.startswith('eddy_') and struct_params.eddy_lmax == 0:
                                der_param_seq = np.zeros((), dtype=complex)
                            elif name == 'eddy_odd':
                                der_param_seq = shell.spherical_harmonics(struct_params.eddy_lmax, odd=True).T.dot(dphase.real)
                            elif name == 'eddy_even':
                                der_param_seq = shell.spherical_harmonics(struct_params.eddy_lmax, odd=False).T.dot(dphase.real)
                            else:
                                der_param_seq = all_derivatives[name][idx_shell][idx_readout](*param_array)
                            if name == 'movement_phase':
                                der_param = der_param_seq * der_signal
                            elif name.startswith('eddy_'):
                                der_param = der_param_seq
                            elif np.asarray(der_param_seq).ndim == 0:
                                der_param = der_param_seq * der_signal.sum()
                            else:
                                der_param = np.dot(der_param_seq, der_signal)
                            idx_start = map_derivative[(name, idx_shell, idx_fibre)]
                            dp[edges[idx_start]:edges[idx_start+1]] += der_param.real
            return ct, dp
        return cost, convert_params, init


@lru_cache(maxsize=None)
def _lambdify_equation_cached(params, equation, name=None):
    """
    Cached function to convert sympy equations into numpy functions

    Used internally by `Model.funcs`.
    """
    if name is not None:
        equation = sym.diff(equation, name)
    return sym.lambdify(params, equation, 'numpy')


def alignment(phi, theta, bvec, sympy=True):
    """
    Computes the dot-product between the fibre alignment and the gradient orientation

    :param phi: angle in x-y plane (longitude)
    :param theta: angle with respect to z-axis (latitude)
    :param bvec: (..., 3) array with gradient orientations
    :param sympy: set to True for sympy input, False for numpy input
    :return: (..., ) array with dot-product
    """
    m = sym if sympy else np
    return (
            m.cos(phi) * m.sin(theta) * bvec[0] +
            m.sin(phi) * m.sin(theta) * bvec[1] +
            m.cos(theta) * bvec[2]
    )


def myelin_phase(shell, phi, theta, mean_log_g, sympy=True):
    """
    Computes the intra-axonal phase accumulation due to myelin in rad

    :param shell: acquisition details
    :param phi: fibre angle
    :param theta: fibre angle
    :param mean_log_g: average log(g) in the fibre population
    :param sympy: set to True for sympy input, False for numpy input
    :return: phase accumulated at second readout in rad
    """
    return -0.75 * shell.scanner.larmor_frequency * mean_log_g * (
            1 - alignment(phi, theta, shell.b0_dir, sympy) ** 2) * shell.scanner.anisotropic_susceptibility * 1e-9 * shell.t_phase


def single_fit(parameters: Parameters, data, tofit, model: Model, scipy_kwargs=None, only_mag=False,
               verbose=False) -> Parameters:
    """
    Local fit of parameters using `scipy.optimize.minimize`

    :param parameters: initial guess of parameters (and acquisition parameters)
    :param data: for each shell a length 2 sequence with the signal in both readouts
    :param tofit: sequence of which parameters to fit
    :param model: model to fit to the data
    :param scipy_kwargs: keyword arguments to pass on to scipy
    :param only_mag: if True only consider the magnitude (no complex signal)
    :param verbose: if True report on intermediate fits (2 for very verbose)
    :return: updated estimate of parameters
    """
    if scipy_kwargs is None:
        scipy_kwargs = {}
    bounds = get_bounds(parameters, tofit)
    f, cf, init = model.get_cost(parameters, data, tofit, only_mag=only_mag)
    if verbose:
        print(f"Optimising {tofit}")
    best_fit = optimize.minimize(f, init, jac=True, bounds=bounds, **scipy_kwargs)
    if verbose:
        print(best_fit.message, best_fit.fun)
        if verbose >= 2:
            print(best_fit)
    return cf(best_fit.x)


def estimate_eddy(current_fit: Parameters, data):
    """
    Estimates the first-order spherical harmonic components of the eddy currents

    :param current_fit: current best fit parameters. The first three values of eddy_odd are updated in place.
    :param data: for each shell a length 2 sequence with the signal in both readouts
    """
    for (shell, shell_params), shell_data in zip(current_fit, data):
        ref_phase = shell_params[0]['movement_phase']
        delta_phase = np.angle(shell_data[1]) - ref_phase
        grad = eddy_gradient(abs(shell_data[1]) * np.exp(1j * delta_phase), shell.gradients)
        eddy_odd = np.array(shell_params[0]['eddy_odd'])
        eddy_odd[:3] = grad[[0, 2, 1]] * np.sqrt(np.pi / 0.75) * [-1, 1, -1]
        shell_params[0]['eddy_odd'] = np.asarray(eddy_odd)


def eddy_gradient(complex_signal, bvecs):
    """
    Estimates the phase gradient with bvecs

    :param complex_signal: (N, ) array with complex signal
    :param bvecs: (N, 3) array with gradient orientations (should all be unit length)
    :return: (3, ) array with the gradients
    """
    phase = np.angle(complex_signal)
    hull = spatial.ConvexHull(bvecs)
    dphase = []
    dg = []
    magnitude = []
    for idx1 in range(3):
        for idx2 in range(idx1):
            v1, v2 = hull.simplices[:, idx1], hull.simplices[:, idx2]
            dp = phase[v1] - phase[v2]
            dp[dp < -np.pi] += np.pi * 2
            dp[dp > np.pi] -= np.pi * 2
            dphase.append(dp)
            dg.append(bvecs[v1] - bvecs[v2])
            magnitude.append(abs(complex_signal)[v1] + abs(complex_signal)[v2])
    weight = np.concatenate(magnitude, 0) ** 2
    return np.linalg.lstsq(weight[:, None] * np.concatenate(dg, 0), weight * np.concatenate(dphase, 0), rcond=None)[0]


def global_fit(best_fit: Parameters, data, tofit, model:Model) ->Parameters:
    """
    Global fit to the chosen parameters using dual annealing

    :param best_fit: best fit in the optimisation so far
    :param data: for each shell a length 2 sequence with the signal in both readouts (complex if only_mag is False)
    :param tofit: sequence of which parameters to fit
    :param only_mag: if True only consider the magnitude (no complex signal)
    :param fit_T2: if True use the values for R2 & R2i, rather than R2_attenuation
    :param dual_phase: if True use the dual population rather than single population model for log(g)
    :param even_eddy: if True include the effect of the even component of the eddy current spherical harmonics
    :return: new set of parameters after global optimisation
    """
    bounds = get_bounds(best_fit, tofit)
    print('starting global fit')
    f, cf, _ = model.get_cost(best_fit, data, tofit)
    res = optimize.dual_annealing(f, bounds,  local_search_options={'jac': True}, maxiter=1000)
    print(res.message, res.fun)
    return cf(res.x)


def get_bounds(parameters: Parameters, tobound):
    """
    Defines the bounds

    :param parameters: any set of parameters including definition of the acquisition
    :param tobound: names of parameters for which bounds will be returned
    :return: sequence of tuples with lower and upper bound for each parameter
    """
    use_bounds = False
    bounds_vals = {
        'log_g': (np.log(0.5), np.log(1.2)),
        'log_g_myelin': (np.log(0.5), np.log(1)),
        'f_myelin': (0, 1),
    }

    bounds = []
    for name in tobound:
        if name in bounds_vals:
            use_bounds = True
        nvals = np.sum([arr.size for arr in parameters.to_change([name])[0]])

        bounds.extend([bounds_vals.get(name, (-np.inf, np.inf))] * nvals)
    if not use_bounds:
        return None
    return bounds


def fit(parameters, data, model: Model, even_eddy=False, only_myelin=False, movement_phase=True,
        nfit=100, return_all=False, fit_2D=False, verbose=False) -> Parameters:
    """
    Multi-step fitting procedure for diffusion-weighted phase data in a single voxel

    :param parameters: acquisition parameters (can be created from :func:`Parameters.empty`)
    :param data: for each shell a length 2 sequence with the signal in both readouts (complex if only_mag is False)
    :param model: which model to fit to the data
    :param even_eddy: if True include the effect of the even component of the eddy current spherical harmonics
    :param only_myelin: don't fit the non-myelin contribution to the phase
    :param movement_phase: include random phase offsets before the first readout
    :param nfit: maximum number of fits during global optimisation
    :param return_all: return all local fits of global optimisation rather than just be best one
    :param fit_2D: fits data with gradients only in the x-y plane
    :param verbose: if True report on intermediate fits (2 for very verbose)
    :return: best-fit parameters
    """
    # fitting magnitude data
    l = locals()
    if fit_2D:
        for _, shell_params in parameters:
            for fibre_params, phi in zip(shell_params, np.linspace(0, np.pi, parameters.nfibres + 1)):
                fibre_params['theta'] = np.pi/2.
                fibre_params['phi'] = phi
        angles = ('phi', )
    else:
        #parameters.guess_orient(data)
        angles = ('theta', 'phi')
    #print("orientation after DTI:", parameters.as_dict['theta'], parameters.as_dict['phi'])
    ase_mags = ('R2', 'R2i') if model.T2 else ('R2_attenuation', )
    best_fit = single_fit(parameters, data, ('amplitude_se', ), model, only_mag=True, verbose=verbose)
    best_fit = single_fit(best_fit, data, ase_mags, model, only_mag=True, verbose=verbose)
    best_fit = single_fit(best_fit, data, ('width', 'amplitude_se') + ase_mags, model, only_mag=True, verbose=verbose)
    best_fit = single_fit(best_fit, data, angles + ('width', 'amplitude_se') + ase_mags, model,
                          only_mag=True, verbose=verbose)

    # fitting phase as well
    if movement_phase:
        for idx_shell, shell_data in enumerate(data):
            best_fit.as_dict['movement_phase'][1][idx_shell] = np.angle(shell_data[0])
    phase_confounds = ['eddy_odd']
    if best_fit.eddy_lmax > 0:
        estimate_eddy(best_fit, data)
    if even_eddy:
        phase_confounds.append('eddy_even')
    if not only_myelin and not model.only_phase:
        phase_confounds.append('non_myelin')

    log_g_vars = ('log_g_myelin', 'f_myelin') if model.dual_phase else (
        ("dphase", ) if model.only_phase else ('log_g', ))
    final_fits = []
    best_value = np.inf
    best_iter_fit = None
    nconsistent = 0
    for _ in range(nfit):
        iter_fit = best_fit.copy()
        for _, params in iter_fit:
            if not only_myelin:
                params[0]['non_myelin'] = np.random.rand() * 4 - 2
            for idx_fibre, pfibre in enumerate(params):
                if model.dual_phase:
                    pfibre['log_g_myelin'] = np.log(np.random.rand() * 0.2 + 0.6)
                    pfibre['f_myelin'] = np.random.rand()
                elif model.only_phase:
                    pfibre['dphase'] = (np.random.rand() * 2 - 1) * np.pi
                else:
                    pfibre['log_g'] = np.log(np.random.rand() * 0.4 + 0.6)
        phase_confounds = tuple(phase_confounds)
        iter_fit = single_fit(iter_fit, data, phase_confounds, model,
                              verbose=verbose)

        final_fits.append(single_fit(iter_fit, data, log_g_vars + phase_confounds, model, verbose=verbose,
                                     scipy_kwargs=dict(options=dict(ftol=1e-9), method='L-BFGS-B')))
        ct = model.cost(final_fits[-1], data)
        consistent = np.isclose(ct, best_value, rtol=1e-1)
        if ct < best_value:
            best_iter_fit = final_fits[-1]
            best_value = ct
            if not consistent:
                nconsistent = 0
        if consistent:
            nconsistent += 1
        if nconsistent >= 5:
            break
    if return_all:
        return final_fits
    else:
        mp = ("movement_phase", ) if movement_phase else ()
        return single_fit(best_iter_fit, data, angles + ('width', ) + mp +
                          log_g_vars + ase_mags + phase_confounds, model, verbose=verbose,
                          scipy_kwargs=dict(options=dict(ftol=1e-13), method='L-BFGS-B'))

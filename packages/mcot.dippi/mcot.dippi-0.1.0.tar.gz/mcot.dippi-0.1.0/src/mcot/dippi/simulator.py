from scipy import stats
import numpy as np
from dataclasses import dataclass, fields
from mcot.maths import spherical
from typing import Sequence
from .scan import SimulatedShell, Encoding


@dataclass
class FibrePopulation:
    """
    Represents a single fibre population with a single orientation and b-value
    """
    """base signal (proton density)"""
    M0: float = 1.

    """Angle in 2D plane"""
    phi: float = 0.

    # relaxometry
    """T2 of water in ms; 60 ms (Wiggermann et al. 2018) at 7T; """
    T2: float = 60.

    """T2i of water due to dephasing in ms; 35 ms (Sati et al. 2013) at 7T;"""
    T2_star: float = 35.

    # diffusion
    """paralled diffusivity in micrometer^2/ms"""
    d_parallel: float = 1.7
    """perpendicular diffusivity in micrometer^2/ms"""
    d_perpendicular = 0.

    """fraction of water in myelinated versus unmeylinated axons"""
    f_myelin: float = 0.5

    """g-ratio of the fibres"""
    g_ratio: float = 0.8

    """Angle of fibre with the z-direction (default orientation for main magnetic field)"""
    theta: float = np.pi / 2

    @property
    def orientation(self, ):
        return spherical.spherical2cart(1., self.phi, self.theta)

    @property
    def T2i(self, ):
        return 1 / (1 / self.T2_star - 1 / self.T2)

    def as_dict(self, fibre_idx):
        """
        Converts all the relevant information into a dictionary

        :param fibre_idx: index of the fibre
        """
        res = {f'fibre{fibre_idx}_true_{field.name}': getattr(self, field.name) for field in fields(self)}
        for prop_name in ['d_perp']:
            res[f'fibre{fibre_idx}_true_{prop_name}'] = getattr(self, prop_name)
        return res


def random_eddy_params(lmax, odd=True):
    """
    Computes the phase offset due to eddy currents

    :param lmax:
    :param odd:
    :return:
    """
    # mean spherical harmonic power over the phantom
    flat_phase = np.array((0.056, 1.94, 0.043, 0.168, 0.009, 0.149, 0.004, 0.07, 0.0087))
    frequency = np.array((0.48, 11.13, 0.036, 0.077, 0.0047, 0.20, 0.011, 0.14, 0.011)) / 30 ** 2
    indices, _ = SimulatedShell.spherical_harmonics_indices(lmax, odd)
    params = np.empty((indices.size, 2))
    for idx in range(indices.size):
        params[idx, 0] = np.random.randn() * np.sqrt(flat_phase[indices[idx]])
        params[idx, 1] = np.random.randn() * np.sqrt(frequency[indices[idx]])
    return params


def random_confounds(shells: Sequence[SimulatedShell], movement=True, eddy_odd=True, eddy_even=False, non_myelin=True,
                     eddy_lmax=6):
    params_even = random_eddy_params(eddy_lmax, odd=False)
    if not eddy_even:
        params_even *= 0
    params_odd = random_eddy_params(eddy_lmax, odd=True)
    if not eddy_odd:
        params_odd *= 0
    ampl_movement = 2 * np.pi if movement else 0
    non_myelin_freq = 10. * non_myelin

    confounds = {'non_myelin': non_myelin_freq,
                 'eddy_even': [],
                 'eddy_odd': [],
                 'movement': [],
                 'eddy_lmax': eddy_lmax}
    for s in shells:
        confounds['eddy_even'].append(params_even[:, 0] + params_even[:, 1] * s.t_phase)
        confounds['eddy_odd'].append(params_odd[:, 0] + params_odd[:, 1] * s.t_phase)
        confounds['movement'].append(np.random.rand(s.ngradients) * ampl_movement)
    return confounds


def stick_magnitude1(scan: SimulatedShell, fibre: FibrePopulation, split_compartments=False):
    """
    Computes the magnitude contributed by a stick at the first readout

    :param scan: sequencing parameters
    :param fibre: fibre population parameters
    :param split_compartments: if True return tuple with intra- and extra-axonal water separately
    :return: total magnitude at first readout
        (or separate intra- and extra-axonal contributions if `split_compartments` is True)
    """
    T2_intra = np.exp(-scan.TE1 / fibre.T2_intra)
    T2_extra = np.exp(-scan.TE1 / fibre.T2_extra)

    if scan.ndim == 2:
        cos_angle = np.cos(scan.gradients - fibre.angle)
    else:
        cos_angle = scan.gradients.dot(fibre.orientation)

    if scan.encoding == Encoding.linear:
        diff_intra = np.exp(-scan.bval * cos_angle ** 2 * fibre.d_parallel)
        diff_extra = np.exp(
            -scan.bval * (cos_angle ** 2 * fibre.d_parallel + (1 - cos_angle ** 2) * fibre.d_perp))
    elif scan.encoding == Encoding.planar:
        diff_intra = np.exp(-scan.bval / 2 * (1 - cos_angle ** 2) * fibre.d_parallel)
        diff_extra = np.exp(
            -scan.bval / 2 * ((1 - cos_angle ** 2) * fibre.d_parallel + (1 + cos_angle ** 2) * fibre.d_perp))
    else:
        raise ValueError(f"Signal modelling for {scan.encoding} not implemented")
    magnitudes = (fibre.f_intra * diff_intra * T2_intra, (1 - fibre.f_intra) * diff_extra * T2_extra)
    if split_compartments:
        return magnitudes
    return magnitudes[0] + magnitudes[1]


def phase_shift(scan, fibre, non_myelin_frequency=0.):
    """
    Computes the phase shift experienced between first and second readout

    :param scan: sequencing parameters
    :param fibre: fibre population parameters
    :return: accumulated phase shift in radians
    """
    extra_internal_freq = scan.scanner.intra_axonal_frequency(fibre.g_ratio, fibre.angle_b0)
    return (extra_internal_freq + non_myelin_frequency) * scan.t_phase


def stick_signal2(scan, fibre, split_compartments=False, non_myelin=0):
    """
    Computes the signal/phase contributed by a stick at the second readout

    :param scan: sequencing parameters
    :param fibre: fibre population parameters
    :param split_compartments: if True return tuple with intra- and extra-axonal water separately
    :param non_myelin: off-resonance frequency from non-myelin sources
    :return: total signal as complex number at second readout
        (or separate intra- and extra-axonal contributions if `split_compartments` is True)
    """
    intra1, extra1 = stick_magnitude1(scan, fibre, split_compartments=True)
    mag_intra = intra1 * (
            np.exp(-(scan.TE2 - scan.TE1) / fibre.T2_intra) *
            np.exp(-scan.t_phase * 1. / fibre.T2i_intra)
    )
    mag_extra = extra1 * (
            np.exp(-(scan.TE2 - scan.TE1) / fibre.T2_extra) *
            np.exp(-scan.t_phase * 1. / fibre.T2i_extra)
    )

    intra_phase = phase_shift(scan, fibre)

    compartments = (
        mag_intra * np.exp(1j * intra_phase), mag_extra * np.exp(1j * non_myelin * scan.t_phase)
    )
    if split_compartments:
        return compartments[0], compartments[1]
    return compartments[0] + compartments[1]


def single_shell(pv_fibres, fibres: Sequence[FibrePopulation], shell: SimulatedShell = None, confounds=None, noise_level=0):
    """
    Computes the observed signal for N fibres
    
    :param pv_fibres: (N, ) array of partial volume of fibres (should add up to one)
    :param fibres: (N, ) sequence describing each fibre population in the voxel
    :param shell: scan parameters
    :param confounds: dictionary with the confounds
    :param noise_level: noise level to add to the data (relative to M0)
    """
    if shell is None:
        shell = SimulatedShell()
    if confounds is None:
        confounds = random_confounds([shell])

    assert np.sum(pv_fibres) == 1
    mag1 = np.sum([pv * stick_magnitude1(shell, f) for pv, f, in zip(pv_fibres, fibres)], 0)
    signal2 = np.sum([pv * stick_signal2(shell, f, non_myelin=confounds['non_myelin'])
                      for pv, f, in zip(pv_fibres, fibres)], 0)

    diff_phase_shift = confounds['movement'][0]
    shifted_signal1 = mag1 * np.exp(1j * diff_phase_shift)

    phase_eddy = (
            shell.spherical_harmonics(confounds['eddy_lmax'], odd=False).dot(confounds['eddy_even'][0]) +
            shell.spherical_harmonics(confounds['eddy_lmax'], odd=True).dot(confounds['eddy_odd'][0])
    )
    shifted_signal2 = abs(signal2) * np.exp(1j * (diff_phase_shift + phase_eddy + np.angle(signal2)))
    np.testing.assert_allclose(abs(shifted_signal1), mag1)

    if noise_level > 0:
        to_complex = np.vectorize(np.complex)
        shifted_signal1 += to_complex(*np.random.randn(2, shell.ngradients)) * noise_level
        shifted_signal2 += to_complex(*np.random.randn(2, shell.ngradients)) * noise_level

    return shifted_signal1, shifted_signal2


def model_signal(pv_fibres, fibres: Sequence[FibrePopulation], shells: Sequence[SimulatedShell], confounds=None, noise_level=0):
    if confounds is None:
        confounds = random_confounds(shells)
    data = []
    for idx, shell in enumerate(shells):
        single_confounds = {name: [value[idx]] if isinstance(value, list) else value
                            for name, value in confounds.items()}
        data.append(single_shell(pv_fibres, fibres, shell, single_confounds, noise_level))
    return data


def simulation_signal(trajectories: np.ndarray, geometry, shell: SimulatedShell, bvecs,
                      R2=1/60., R2_star=1/35., phase_prime=False,
                      global_phase=0., bulk_sigma=0):
    """
    Simulate the signal from Camino simulation

    :param trajectories: structured array with the result from the simulation (loaded using `mcutils.utils.trajectory`)
        Should contain the time in seconds and 3-dimensional locations of each spin in meter
    :param geometry: the geometry used to model the susceptibility field and separate intra- from extra-axonal axons
    :param shell: Scanning parameters
    :param bvecs: (N, 3) array with gradient orientations
    :param R2: irreversible dephasing in kHz (i.e., 1/ms)
    :param R2_prime: reversible dephasing in kHz (i.e., 1/ms)
    :param phase_prime: model reversible dephasing as Lorentzian distribution of off-resonance frequencies
    :param global_phase: global off-frequency offset in fraction of the Larmor frequency
    :param bulk_sigma: size of the Guassian distribution from which to draw the bulk linear motion in micrometer/ms
    :return: structure array with for every timepoint:

        - "time": time in ms
        - "total": total signal (complex number for each gradient orientation)
        - "extra": total extra-axonal signal (complex number for each gradient orientation)
        - "intra": total intra-axonal signal (complex number for each gradient orientation and axon population)
    """
    bvecs = bvecs / np.sum(bvecs ** 2, -1)[:, None]
    assert bvecs.shape[1] == 3
    assert bvecs.ndim == 2
    n_spins, n_stored = trajectories.shape
    n_steps = n_stored - 1

    diffusion_frequency = np.zeros(n_steps)
    time = trajectories[0]['time'] * 1e3
    assert np.argmax(time) == (time.size - 1), "Time array appears to be incomplete. Did the simulation finish?"
    if shell.dual_echo:
        dephase_time = np.amin((time, abs(time - shell.TE1), abs(time - shell.TE2)), 0)
    else:
        dephase_time = np.amin((time, abs(time - shell.TE1)), 0)

    for start in (
            shell.scanner.t_pulse / 2.,
            shell.scanner.t_pulse / 2. + shell.t_diff1 + shell.scanner.t_pulse
    ):
        end = start + shell.t_diff2
        within = (time > start) & (time < end)
        diffusion_frequency[within[1:] & within[:-1]] = 1.
        idx_start = np.where(time > start)[0][0]
        diffusion_frequency[idx_start - 1] = (time[idx_start] - start) / (time[idx_start] - time[idx_start - 1])
        idx_end = np.where(time > end)[0][0]
        diffusion_frequency[idx_end - 1] = (end - time[idx_end - 1]) / (time[idx_end] - time[idx_end - 1])
        if idx_end == idx_start:
            diffusion_frequency[idx_end - 1] = (end - start) / (time[idx_end] - time[idx_end - 1])
    diffusion_frequency *= shell.scanner.max_gradient

    # apply refocus pulse
    frequency_sign = np.ones(n_steps)
    idx_te1 = np.where(time > shell.refocus1)[0][0]
    frequency_sign[:idx_te1 - 1] = -1.
    frequency_sign[idx_te1 - 1] = 2 * (time[idx_te1] - shell.refocus1) / (time[1] - time[0]) - 1
    if shell.dual_echo:
        idx_te2 = np.where(time > shell.refocus2)[0][0]
        frequency_sign[:idx_te2 - 1] *= -1
        frequency_sign[idx_te2 - 1] = -2 * (time[idx_te2] - shell.refocus2) / (time[1] - time[0]) + 1

    res = np.zeros(n_stored, dtype=[
        ('time', 'float'),
        ('total', ('complex', len(bvecs))),
        ('extra', ('complex', len(bvecs))),
        ('intra', ('complex', (2, len(bvecs)))),
    ])
    res['time'] = time

    # bulk linear motion
    bulk = np.random.randn(len(bvecs), 3) * bulk_sigma

    for idx, path in enumerate(trajectories):
        within_axon = geometry.in_axon(path['pos'])
        for internal in within_axon:
            assert internal.all() or not internal.any()
        within_axon = np.array([internal.any() for internal in within_axon])

        mean_pos = (path['pos'][1:] + path['pos'][:-1]) / 2.
        phase_offset = frequency_sign * (
                (geometry(mean_pos) + global_phase) * shell.scanner.B0 * 1e3 +
                diffusion_frequency * np.sum(bvecs[:, None, :] * (
                mean_pos[None, :, :] +
                np.random.rand(3, ) * 1e-3 +  # give spin random position within voxel
                bulk[:, None, :] * time[None, :-1, None] * 1e-6), -1)
        ) * shell.scanner.gyro_magnetic_ratio * (time[1] - time[0])

        magnitude = np.exp(-time * R2) / n_spins

        R2_prime = R2_star - R2
        if phase_prime:
            phase_offset += frequency_sign * stats.cauchy.rvs(scale=R2_prime) * (time[1] - time[0])
        else:
            magnitude *= np.exp(-dephase_time * R2_prime)

        phase = np.concatenate((np.zeros((bvecs.shape[0], 1)), np.cumsum(phase_offset, axis=-1)), axis=-1)
        signal = magnitude[None, :] * np.exp(1j * phase)
        res['total'] += signal.T
        if not within_axon.any():
            res['extra'] += signal.T
        else:
            for idx_intra in np.where(within_axon)[0]:
                res['intra'][:, idx_intra, :] += signal.T
    return res

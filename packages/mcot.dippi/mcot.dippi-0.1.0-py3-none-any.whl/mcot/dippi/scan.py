"""
Defines the acquisition parameters for a shell of DIPPI data
"""
from enum import Enum
from scipy import optimize
from dataclasses import dataclass, InitVar, field
import numpy as np
from fsl.wrappers import gps, LOAD
from dipy.reconst import shm
from mcot.maths import spherical
from typing import Sequence
from dataclasses_json import DataClassJsonMixin, config
import xarray
import pandas as pd
from typing import Union


class Encoding(Enum):
    """
    Type of diffusion encoding to use
    """
    linear = 1
    planar = 2


@np.vectorize
def linear_bfun(t_diff2, G, slew, t_pulse=5., t_ro=50., gamma=267.5):
    """
    Estimates the b-value based on the timings

    :param t_diff2: time for diffusion gradient between refocus pulse and readout (in ms)
    :param G: maximum gradient strength in mT/m
    :param slew: maximal change of gradient strength in mT/m/ms
    :param t_pulse: time duration of excitation and refocus pulse (in ms)
    :param t_ro: readout time in ms
    :param gamma: gyromagnetic constant in rad/ms/mT
    :return: b-value in ms/micrometer^2
    """
    delta = t_diff2 - G / slew
    if delta < 0:
        return np.nan
    TE1 = 2 * (t_diff2 + 0.5 * (t_pulse + t_ro))
    Delta = TE1 / 2.
    return (gamma * 1e-6 * G * delta) ** 2 * (Delta - delta / 3)  # 1e-6 converts from meter to micrometer


@dataclass(unsafe_hash=True)
class Scanner(DataClassJsonMixin):
    """
    Properties of a single fibre population
    """
    """Precession speed in rad/ms/mT"""
    gyro_magnetic_ratio: float = 267.5

    """anisotropic susceptibility of myelin in ppb"""
    anisotropic_susceptibility: float = -100

    """strength of the magnetic field"""
    B0: float = 7.

    # diffusion encoding
    """maximum gradient strength in mT/m"""
    max_gradient: float = 80.
    """maximum slew rate in mT/m/ms"""
    slew_rate: float = 200.

    # sequence timings
    """Duration of the excitation and refocus pulses in ms"""
    t_pulse: float = 5.
    """Duration of the readout in ms"""
    t_ro: float = 50.

    @property
    def larmor_frequency(self, ):
        """Larmor frequency in rad/ms"""
        return self.gyro_magnetic_ratio * self.B0 * 1e3

    def intra_axonal_frequency(self, g_ratio, angle_b0):
        """Computes the frequency within an axon in rad/ms

        :param g_ratio: g-ratio of the axon
        :param angle_b0: angle between the axon the main magnetic field
        """
        return -0.75 * self.larmor_frequency * np.log(g_ratio) * np.sin(angle_b0) ** 2 * self.anisotropic_susceptibility * 1e-9


@dataclass(unsafe_hash=True)
class ObservedShell(DataClassJsonMixin):
    """
    Represents an shell of actual observed data
    """
    """Orientation of diffusion-weighted gradients in (N, 3) array"""
    gradients: np.ndarray

    """Properties of the scanner on which the data was acquired"""
    scanner: Scanner = field(default_factory=Scanner)

    """b-value in ms/micrometer^2"""
    bval: float = 3.

    """Whether to add a second refocus pulse"""
    dual_echo: bool = True

    """time of phase accumulation"""
    t_phase: float = 30

    """direction of the B0 field"""
    b0_dir: np.ndarray = np.array([0, 0, 1.])

    """Give each shell that should be considered a different orientation a different b0_group"""
    b0_group: int = 0

    """Time of first spin echo in ms"""
    TE1: float = 80

    """Time of second spin echo in ms"""
    TE2: float = 120

    @property
    def readout1(self, ):
        """Time of first readout in ms"""
        return self.TE1

    @property
    def readout2(self, ):
        """Time of second readout in ms"""
        return self.TE2 + self.t_phase

    def spherical_harmonics(self, lmax, odd=True):
        return spherical_harmonics(self.gradients, lmax, odd)

    @property
    def ngradients(self, ):
        return self.gradients.shape[0]


@dataclass(unsafe_hash=True)
class SimulatedShell(DataClassJsonMixin):
    """
    Represents the scan settings and physical constants

    Used in both the simulator and in fitting

    This represents a single shell of diffusion-weighted susceptibility data

    The main scanner parameters to be set are B0, max_gradient, slew_rate, and
    the duration of the readout (t_ro) and pulse (t_pulse)

    The main acquisition parameters to be set are bval, t_phase, and gradients.
    The gradients can be initialised uniformly by settings ngradients_in.

    The second refocus pulse can be removed by setting dual_echo to false (will raise an error if t_ro > t_phase)

    Based on this input the following times are computed
    - TE1 = readout1: time of first spin echo/readout
    - TE2: time of second spin echo (only if dual_echo=True)
    - readout2: time of second readout (=echo time + t_phase)
    - time_done: time the second readout is finished (readout2 + t_ro/2)
    """
    """Properties of the scanner on which the data was acquired"""
    scanner: Scanner = field(default_factory=Scanner)

    # diffusion encoding
    """Type of encoding (linear or planar)"""
    encoding: Encoding = Encoding.linear
    """b-value in ms/micrometer^2"""
    bval: float = 3.
    """Gradients orientations (1D array for angles in 2D-plane or (N, 3) array for full gradient orientations)"""
    gradients: np.ndarray = field(default=None, hash=False, repr=False, compare=False,
                                  metadata=config(
                                      encoder=lambda a: [[c for c in b] for b in a],
                                      decoder=np.array,
                                  ))

    """Helper parameters to define a default set of bvecs (if user does not provide one)"""
    ngradients_in: InitVar[int] = 30
    ndim_in: InitVar[int] = 3

    # other parameters
    """Whether to add a second refocus pulse"""
    dual_echo: bool = True

    """time of phase accumulation"""
    t_phase: float = 30

    """angle of B0 with the z-direction (assumed in x-z plane)"""
    theta_b0: float = 0.

    def __post_init__(self, ngradients_in: int, ndim_in: int):
        """Generate uniform gradients if not provided"""
        if self.gradients is None:
            if ndim_in == 2:
                self.phi = np.linspace(0, np.pi, ngradients_in + 1)[:-1]
                self.gradients = np.stack([np.cos(self.phi), np.sin(self.phi), np.zeros(ngradients_in)], -1)
            elif ndim_in == 3:
                self.gradients = gps(LOAD, ngradients_in, optws=True)['out']
            else:
                raise ValueError(f"number of dimensions should be 2 or 3, not {ndim_in}")
        self._shm = {}

    def spherical_harmonics(self, lmax, odd=True):
        if self.ndim == 2:
            raise ValueError("Spherical harmonics are only supported in 3D")
        if (lmax, odd) not in self._shm:
            self._shm[(lmax, odd)] = spherical_harmonics(self.gradients, lmax, odd)
        return self._shm[(lmax, odd)]

    @property
    def b0_dir(self, ):
        return np.array([np.sin(self.theta_b0), 0., np.cos(self.theta_b0)])

    @property
    def b0_group(self, ):
        return self.theta_b0

    @property
    def ndim(self, ):
        """Whether gradients are on a circle (2) or sphere (3)"""
        return self.gradients.ndim + 1

    @property
    def ngradients(self):
        """Number of gradient orientations in this shell"""
        return self.gradients.shape[0]

    @property
    def t_diff2(self, ) -> float:
        """
        Total duration of pulse (with ramp-up and ramp-down) in ms

        For maximum efficiency this matches the time between the end of the first refocus pulse
        and the start of the first readout.
        """
        if self.bval == 0:
            return 0.
        if self.encoding == Encoding.planar:
            raise NotImplementedError("TODO: encode planar encoding")
        elif self.encoding == Encoding.linear:
            res = optimize.root_scalar(
                lambda td2: self.bval - linear_bfun(td2, self.scanner.max_gradient,
                                                    self.scanner.slew_rate, self.scanner.t_pulse, self.scanner.t_ro),
                bracket=(self.scanner.max_gradient / self.scanner.slew_rate, 50))
            assert res.converged
            return res.root
        raise ValueError("Unrecognised encoding")

    @property
    def TE1(self, ):
        """Time till first readout in ms"""
        return 2 * (self.t_diff2 + 0.5 * (self.scanner.t_pulse + self.scanner.t_ro))

    @property
    def readout1(self, ):
        """Time till the centre of the first readout in ms

        same as TE1
        """
        return self.TE1

    @property
    def t_diff1(self, ):
        """Time between end of excitation and start of refocus pulse in ms"""
        return self.TE1 / 2. - self.scanner.t_pulse

    @property
    def refocus1(self, ):
        """Time of the centre of the first refocus pulse"""
        return self.TE1 / 2.

    @property
    def refocus2(self, ):
        """Time of the centre of the second refocus pulse"""
        if not self.dual_echo:
            raise ValueError("Only single refocus pulse if dual echo is not set to True")
        return self.TE1 + (self.scanner.t_ro + self.scanner.t_pulse) / 2.

    @property
    def TE2(self, ):
        """Time till second readout"""
        if self.dual_echo:
            return self.TE1 + self.scanner.t_ro + self.scanner.t_pulse
        else:
            raise ValueError("`dual_echo` is False, so there is no second echo")
            if self.scanner.t_ro > self.scanner.t_phase:
                raise ValueError("The two readouts overlap. Please switch to dual echo for such short phase accumulation time.")
            return self.TE1

    @property
    def readout2(self, ):
        """Time till the second readout in ms

        echo time + t_phase
        """
        if self.dual_echo:
            return self.TE2 + self.t_phase
        else:
            if self.scanner.t_ro > self.t_phase:
                raise ValueError("The two readouts overlap. Please switch to dual echo for such short phase accumulation time.")
            return self.TE1 + self.t_phase

    @property
    def time_done(self, ):
        """
        Time from the excitation pulse till the end of the second readout in ms
        """
        return self.readout2 + self.scanner.t_ro / 2


def spherical_harmonics(gradients, lmax, odd=True):
    n_list, m_list = spherical_harmonics_indices(lmax, odd)
    _, phi, theta = spherical.cart2spherical(*gradients.T)
    return shm.real_sph_harm(m_list, n_list, theta[:, None], phi[:, None])


def spherical_harmonics_indices(lmax, odd=True):
    n_range = np.arange(1 if odd else 2, lmax + 1, 2)
    n_list = np.repeat(n_range, n_range * 2 + 1)
    m_list = []
    for ii in n_range:
        m_list.extend(range(-ii, ii + 1))
    return n_list, np.array(m_list)


Shell = Union[ObservedShell, SimulatedShell]


class MultiShell(object):
    def __init__(self, shells: Sequence[Shell], group_by=('bval', 'b0_group', 't_phase')):
        """
        Represents multiple shells acquired in the same scan

        :param shells: individual shells scanned
        """
        self.shells = shells
        self.group_by = group_by

        self.possible_values = tuple(sorted({getattr(shell, name) for shell in shells})
                                     for name in self.group_by)
        indices = -np.ones([len(values) for values in self.possible_values], dtype=int)
        for idx_shell, shell in enumerate(shells):
            idx = tuple(values.index(getattr(shell, name)) for name, values in self.coords)
            indices[idx] = idx_shell
        self.indices = xarray.DataArray(indices, self.coords)
        self.available = self.indices >= 0

    def to_list(self, ):
        return [s.to_dict(encode_json=True) for s in self.shells]

    @property
    def coords(self, ):
        return [(name, values) for name, values in zip(self.group_by, self.possible_values)]

    @property
    def coords1d(self, ):
        return pd.MultiIndex.from_arrays([[getattr(s, name) for s in self.shells] for name in self.group_by],
                                         names=self.group_by)

    @classmethod
    def from_list(cls, a_list):
        return cls([SimulatedShell.from_dict(s) for s in a_list])

    def to_json(self, **kwargs):
        return SimulatedShell.schema().dumps(self.shells, many=True, **kwargs)

    @classmethod
    def from_json(cls, text, **kwargs):
        return cls(SimulatedShell.schema().loads(text, many=True, **kwargs))

    def __eq__(self, other):
        if not isinstance(other, MultiShell):
            return NotImplemented
        return self.shells == other.shells

    def enumerated(self, ):
        for shell in self.shells:
            indices = [values.index(getattr(shell, name)) for name, values in self.coords]
            yield indices, shell

    def __getitem__(self, item):
        return self.shells[item]

    def __len__(self, ):
        return len(self.shells)



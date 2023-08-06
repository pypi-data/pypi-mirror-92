"""
Computes the susceptibility field for regularly packed cylinders
"""
import numpy as np
from scipy import interpolate


class PackedCylinders:
    """
    Models regularly packed cylinders with varying g-ratio's and orientations
    """
    def __init__(self, gratios=0.7, angles=(0., np.pi/2.), b0=(0, 1, 0), radius=0.5, spacing=1., 
                 chi_iso=-1e-7, chi_aniso=-1e-7):
        """
        Defines a set of packed cylinders

        :param gratios: 2D array with sequence of g-ratio (first dimension is misaligned with angles,
            second dimension is the same along which angles vary, i.e. y-axis).
        :param angles: Angle of axons around the y-axis for fibres stacked above each other in y-axis (0 means pointing in z-direction)
        :param b0: vector with the main magnetic field orientation
        :param radius: radius of the axons
        :param spacing: spacing between the axon centres
        :param chi_iso: isotropic susceptibility of the myelin
        :param chi_aniso: anisotropic susceptibility of the myelin
        """
        if np.array(gratios).ndim == 1:
            gratios = np.array(gratios)[:, None]
        else:
            gratios = np.atleast_2d(gratios)
        assert gratios.ndim == 2
        angles = np.atleast_1d(angles)
        assert angles.ndim == 1
        ny = np.lcm(gratios.shape[1], angles.shape[0])
        self.gratios = np.tile(gratios, (1, ny // gratios.shape[1]))
        self.angles = np.tile(angles, ny // angles.shape[0])
        self.b0 = np.array(b0) / np.sqrt(np.sum(np.array(b0) ** 2))
        self.radius = radius
        self.spacing = spacing
        self.chi_iso = chi_iso
        self.chi_aniso = chi_aniso
        self.recompute_external_phase()

    @property
    def n_repeat(self, ):
        return self.gratios.shape

    def recompute_external_phase(self, npoints=100, maxrepeat=50):
        """
        Computes and sets the phase due to external axons
        """
        backup_phase = self.external_phase(npoints, maxrepeat)
        x = np.linspace(0, self.n_repeat[0], self.n_repeat[0] * npoints + 1)
        y = np.linspace(0, self.n_repeat[1], self.n_repeat[1] * npoints + 1)
        self.interp_external = [interpolate.RectBivariateSpline(x, y, bphase)
                                for bphase in backup_phase]

    def external_phase(self, npoints, maxrepeat=50):
        """
        Computes the phase due to the contributions of any axons outside of the periodic block

        :param npoints: density of point per spacing (in 1D)
        :param maxrepeat: maximum number of repeats
        :return: (n_repeat[1], n_repeat[0] * npoints, n_repeat[1] * npoints) array with the phase
        """
        phase = np.zeros((self.n_repeat[1], self.n_repeat[0] * npoints + 1, self.n_repeat[1] * npoints + 1))
        for idx, angle, gratio_line in zip(np.arange(self.n_repeat[1]), self.angles, self.gratios.T):
            xgrid = (np.arange(-maxrepeat, maxrepeat + 1, 1) + 0.5) * self.spacing
            idx_start, = np.where(xgrid == 0.5 * self.spacing)[0]
            all_gratio = np.zeros(xgrid.size)
            for idxg, g in enumerate(gratio_line):
                all_gratio[(idx_start + idxg) % self.n_repeat[0]::self.n_repeat[0]] = g
            ygrid_half = np.arange(0, maxrepeat + 1, self.n_repeat[1])
            ygrid = (np.concatenate((-ygrid_half[::-1], ygrid_half[1:]), 0) + idx + 0.5) * self.spacing

            x = np.linspace(0, self.n_repeat[0], self.n_repeat[0] * npoints + 1)
            y = np.linspace(0, self.n_repeat[1], self.n_repeat[1] * npoints + 1)
            xx, yy = np.meshgrid(x, y, indexing='ij')

            s_squared = 1 - (np.sin(angle) * self.b0[0] + np.cos(angle) * self.b0[2]) ** 2

            rsquared = (xx[:, :, None, None] - xgrid[:, None]) ** 2 + (yy[:, :, None, None] - ygrid[None, :]) ** 2
            rsquared[rsquared < self.radius ** 2] = np.inf
            phi = np.arctan2(xx[:, :, None, None] - xgrid[:, None], yy[:, :, None, None] - ygrid[None, :])

            phase[idx] = np.sum(
                s_squared * np.cos(2 * phi) / 2. * self.radius ** 2 / rsquared *
                (1 - all_gratio[:, None] ** 2) * (self.chi_iso + self.chi_aniso / 4.),
                axis=(-2, -1)
            )

        return phase

    def in_axon(self, positions):
        """
        Computes which spins are inside the axons

        :param positions: (..., 3) array with the positions of the spins
        :return: n_repeat[1] iteration of (...) boolean arrays which are true of positions are inside of the axons
        """
        res = []
        for y, angle in enumerate(self.angles):
            proj_y = positions[..., 1] % (self.n_repeat[1] * self.spacing)
            proj_x = (positions[..., 0] * np.cos(angle) - positions[..., 2] * np.sin(angle)) % self.spacing
            rsquared = (proj_x - 0.5 * self.spacing) ** 2 + (proj_y - (y + 0.5) * self.spacing) ** 2
            res.append(rsquared < self.radius ** 2)
        return tuple(res)

    def __call__(self, positions):
        """
        Computes the phase shift at the positions

        :param positions: (..., 3) array with the positions of the spins
        :return: (..., ) array with the phase
        """
        phase = np.zeros(positions.shape[:-1])
        for x, gratio_line in enumerate(self.gratios):
            for y, angle, gratio, bphase in zip(np.arange(self.n_repeat[1]), self.angles, gratio_line, self.interp_external):
                proj_y = positions[..., 1] % (self.n_repeat[1] * self.spacing)
                proj_x = (positions[..., 0] * np.cos(angle) - positions[..., 2] * np.sin(angle)) % (self.n_repeat[0] * self.spacing)
                phase += bphase(proj_x.flatten(), proj_y.flatten(), grid=False).reshape(proj_x.shape)
                rsquared = (proj_x - (x + 0.5) * self.spacing) ** 2 + (proj_y - (y + 0.5) * self.spacing) ** 2

                s_squared = 1 - (np.sin(angle) * self.b0[0] + np.cos(angle) * self.b0[2]) ** 2
                in_axon = rsquared < self.radius ** 2
                phase[in_axon] -= self.chi_aniso * (3 * s_squared) / 4. * np.log(gratio)
        return phase

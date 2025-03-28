__author__ = "sibirrer"

import numpy as np
from lenstronomy.LensModel.Profiles.base_profile import LensProfileBase

__all__ = ["SIS_truncate"]


class SIS_truncate(LensProfileBase):
    """This class contains the function and the derivatives of the truncated Singular Isothermal Sphere potential:

    .. math::
        \\psi(x, y) = 
        \\begin{cases} 
        \\theta_{E} \\, r & r < r_{\\text{trunc}} \\\\
        \\theta_{E} \\, r_{\\text{trunc}} + \\frac{1}{2} \\theta_{E} \\left(3 - \\frac{r}{r_{\\text{trunc}}}\\right) (r - r_{\\text{trunc}}) & r_{\\text{trunc}} \\leq r < 2 r_{\\text{trunc}} \\\\
        \\frac{3}{2} \\theta_{E} \\, r_{\\text{trunc}} & r \\geq 2 r_{\\text{trunc}}
        \\end{cases}

    where :math:`\\theta_{E}` is the Einstein radius and :math:`r_{\\text{trunc}}` is the truncation radius
    """

    param_names = ["theta_E", "r_trunc", "center_x", "center_y"]
    lower_limit_default = {
        "theta_E": 0,
        "r_trunc": 0,
        "center_x": -100,
        "center_y": -100,
    }
    upper_limit_default = {
        "theta_E": 100,
        "r_trunc": 100,
        "center_x": 100,
        "center_y": 100,
    }

    def function(self, x, y, theta_E, r_trunc, center_x=0, center_y=0):
        """
        :param x: set of x-coordinates
        :type x: array of size (n)
        :param y: set of y-coordinates
        :type y: array of size (n)
        :param theta_E: Einstein radius of lens
        :type theta_E: float (in arcsec)
        :param r_trunc: truncated radius
        :type r_trunc: float (in arcsec)
        :param center_x: profile center
        :param center_y: profile center
        :returns:  function
        """

        x_shift = x - center_x
        y_shift = y - center_y
        r = np.sqrt(x_shift * x_shift + y_shift * y_shift)
        if isinstance(r, int) or isinstance(r, float):
            if r < r_trunc:
                f_ = theta_E * r
            elif r < 2 * r_trunc:
                f_ = theta_E * r_trunc + 1.0 / 2 * theta_E * (3 - r / r_trunc) * (
                    r - r_trunc
                )
            else:
                f_ = 3.0 / 2 * theta_E * r_trunc
        else:
            f_ = np.zeros_like(r)
            f_[r < r_trunc] = theta_E * r[r < r_trunc]
            r_ = r[(r < 2 * r_trunc) & (r > r_trunc)]
            f_[(r < 2 * r_trunc) & (r > r_trunc)] = (
                theta_E * r_trunc
                + 1.0 / 2 * theta_E * (3 - r_ / r_trunc) * (r_ - r_trunc)
            )
            f_[r > 2 * r_trunc] = 3.0 / 2 * theta_E * r_trunc
        return f_

    def derivatives(self, x, y, theta_E, r_trunc, center_x=0, center_y=0):
        """Computes the first derivatives df/dx and df/dy.

        :param x: x-coordinate in image plane
        :param y: y-coordinate in image plane
        :param theta_E: Einstein radius of lens
        :param r_trunc: truncated radius
        :type r_trunc: float (in arcsec)
        :param center_x: profile center
        :param center_y: profile center
        :returns: first derivatives (df/dx, df/dy)
        """
        x_shift = x - center_x
        y_shift = y - center_y

        dphi_dr = self._dphi_dr(x_shift, y_shift, theta_E, r_trunc)
        dr_dx, dr_dy = self._dr_dx(x_shift, y_shift)
        f_x = dphi_dr * dr_dx
        f_y = dphi_dr * dr_dy
        return f_x, f_y

    def hessian(self, x, y, theta_E, r_trunc, center_x=0, center_y=0):
        """Computes the Hessian matrix.

        :param x: x-coordinate in image plane
        :param y: y-coordinate in image plane
        :param theta_E: Einstein radius of lens
        :param r_trunc: truncated radius
        :type r_trunc: float (in arcsec)
        :param center_x: profile center
        :param center_y: profile center
        :returns: Hessian matrix components (d^2f/dx^2, d^2f/dxdy, d^2f/dydx, d^2f/dy^2)
        """
        x_shift = x - center_x
        y_shift = y - center_y
        dphi_dr = self._dphi_dr(x_shift, y_shift, theta_E, r_trunc)
        d2phi_dr2 = self._d2phi_dr2(x_shift, y_shift, theta_E, r_trunc)
        dr_dx, dr_dy = self._dr_dx(x, y)
        d2r_dx2, d2r_dy2, d2r_dxy = self._d2r_dx2(x_shift, y_shift)
        f_xx = d2r_dx2 * dphi_dr + dr_dx**2 * d2phi_dr2
        f_yy = d2r_dy2 * dphi_dr + dr_dy**2 * d2phi_dr2
        f_xy = d2r_dxy * dphi_dr + dr_dx * dr_dy * d2phi_dr2
        return f_xx, f_xy, f_xy, f_yy

    def _dphi_dr(self, x, y, theta_E, r_trunc):
        """First derivative of the potential in radial direction.

        :param x: x-coordinate in image plane
        :param y: y-coordinate in image plane
        :param theta_E: Einstein radius of lens
        :param r_trunc: truncated radius
        :type r_trunc: float (in arcsec)
        :returns: derivative dphi/dr
        """
        r = np.sqrt(x * x + y * y)
        if isinstance(r, int) or isinstance(r, float):
            if r == 0:
                a = 0
            elif r < r_trunc:
                a = theta_E
            elif r < 2 * r_trunc:
                a = theta_E * (2 - r / r_trunc)
            else:
                a = 0
        else:
            a = np.zeros_like(r)
            a[(r < r_trunc) & (r > 0)] = theta_E
            r_ = r[(r < 2 * r_trunc) & (r >= r_trunc)]
            a[(r < 2 * r_trunc) & (r >= r_trunc)] = theta_E * (2 - r_ / r_trunc)
            a[r >= 2 * r_trunc] = 0
        return a

    def _d2phi_dr2(self, x, y, theta_E, r_trunc):
        """Second derivative of the potential in radial direction.

        :param x: x-coordinate in image plane
        :param y: y-coordinate in image plane
        :param theta_E: Einstein radius of lens
        :param r_trunc: truncated radius
        :type r_trunc: float (in arcsec)
        :return: second derivative (d^2phi / dr^2)
        """
        r = np.sqrt(x * x + y * y)
        if isinstance(r, int) or isinstance(r, float):
            if r < r_trunc:
                a = 0
            elif r < 2 * r_trunc:
                a = -theta_E / r_trunc
            else:
                a = 0
        else:
            a = np.zeros_like(r)
            a[r < r_trunc] = 0
            a[(r < 2 * r_trunc) & (r > r_trunc)] = -theta_E / r_trunc
            a[r > 2 * r_trunc] = 0
        return a

    def _dr_dx(self, x, y):
        """Derivative dr/dx, dr/dy.

        :param x: x-coordinate in image plane
        :param y: y-coordinate in image plane
        :return: derivatives dr/dx and dr/dy
        """

        r = np.sqrt(x**2 + y**2)
        if isinstance(r, int) or isinstance(r, float):
            if r == 0:
                r = 1
        else:
            r[r == 0] = 1
        return x / r, y / r

    @staticmethod
    def _d2r_dx2(x, y):
        """Second derivatives of dr/dx and dr/dy.

        :param x: x-coordinate in image plane
        :param y: y-coordinate in image plane
        :return: d^2r/dx^2 & d^2r/dy^2
        """
        r = np.sqrt(x**2 + y**2)
        if isinstance(r, int) or isinstance(r, float):
            if r == 0:
                r = 1
        else:
            r[r == 0] = 1
        return y**2 / r**3, x**2 / r**3, -x * y / r**3

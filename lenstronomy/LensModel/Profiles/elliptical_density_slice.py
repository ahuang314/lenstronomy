__author__ = "lynevdv"

import numpy as np
import cmath
from lenstronomy.Util import param_util
from lenstronomy.LensModel.Profiles.base_profile import LensProfileBase

__all__ = ["ElliSLICE"]


class ElliSLICE(LensProfileBase):
    """
    This class computes the lensing quantities for an elliptical slice of constant density.
    Based on Schramm 1994 https://ui.adsabs.harvard.edu/abs/1994A%26A...284...44S/abstract

    Computes the lensing quantities of an elliptical slice with semi major axis 'a' and
    semi minor axis 'b', centered on 'center_x' and 'center_y', oriented with an angle 'psi'
    in radian, and with constant surface mass density 'sigma_0'.
    In other words, this lens model is characterized by the surface mass density :

    ..math::
        \\kappa(x,y) = \\left{
        \\begin{array}{ll}
        \\sigma_0  & \\mbox{if } \\frac{x_{rot}^2}{a^2} + \\frac{y_{rot}^2}{b^2} \\leq 1 \\\
        0 \\& \\mbox{else}
        \\end{array}
        \\right}.

    with

    ..math::
        x_{rot} = x_c \\cos \\psi + y_c \\sin \\psi  \\\
        y_{rot} = - x_c \\sin \\psi + y_c \\cos \\psi  \\\
        x_c = x - center_x  \\\
        y_c = y - center_y

    """

    param_names = ["a", "b", "psi", "sigma_0", "center_x", "center_y"]
    lower_limit_default = {
        "a": 0.0,
        "b": 0.0,
        "psi": -90.0 / 180.0 * np.pi,
        "center_x": -100.0,
        "center_y": -100.0,
    }
    upper_limit_default = {
        "a": 100.0,
        "b": 100.0,
        "psi": 90.0 / 180.0 * np.pi,
        "center_x": 100.0,
        "center_y": 100.0,
    }

    def function(self, x, y, a, b, psi, sigma_0, center_x=0.0, center_y=0.0):
        """Lensing potential.

        :param a: float, semi-major axis, must be positive
        :param b: float, semi-minor axis, must be positive
        :param psi: float, orientation in radian
        :param sigma_0: float, surface mass density, must be positive
        :param center_x: float, center on the x axis
        :param center_y: float, center on the y axis
        """
        kwargs_slice = {
            "center_x": center_x,
            "center_y": center_y,
            "a": a,
            "b": b,
            "psi": psi,
            "sigma_0": sigma_0,
        }
        x_ = x - center_x
        y_ = y - center_y
        x_rot = x_ * np.cos(psi) + y_ * np.sin(psi)
        y_rot = -x_ * np.sin(psi) + y_ * np.cos(psi)
        try:
            len(x_)
        except:
            if (x_rot**2 / a**2) + (y_rot**2 / b**2) <= 1:
                return self.pot_in(x_, y_, kwargs_slice)
            else:
                return self.pot_ext(x_, y_, kwargs_slice)
        else:
            f = np.array(
                [
                    (
                        self.pot_in(x_[i], y_[i], kwargs_slice)
                        if (x_rot[i] ** 2 / a**2) + (y_rot[i] ** 2 / b**2) <= 1
                        else self.pot_ext(x_[i], y_[i], kwargs_slice)
                    )
                    for i in range(len(x_))
                ]
            )
            return f

    def derivatives(self, x, y, a, b, psi, sigma_0, center_x=0.0, center_y=0.0):
        """Lensing deflection angle.

        :param a: float, semi-major axis, must be positive
        :param b: float, semi-minor axis, must be positive
        :param psi: float, orientation in radian
        :param sigma_0: float, surface mass density, must be positive
        :param center_x: float, center on the x axis
        :param center_y: float, center on the y axis
        """
        kwargs_slice = {
            "center_x": center_x,
            "center_y": center_y,
            "a": a,
            "b": b,
            "psi": psi,
            "sigma_0": sigma_0,
        }
        x_ = x - center_x
        y_ = y - center_y
        x_rot = x_ * np.cos(psi) + y_ * np.sin(psi)
        y_rot = -x_ * np.sin(psi) + y_ * np.cos(psi)
        try:
            len(x_)
        except:
            if (x_rot**2 / a**2) + (y_rot**2 / b**2) <= 1:
                return self.alpha_in(x_, y_, kwargs_slice)
            else:
                return self.alpha_ext(x_, y_, kwargs_slice)
        else:
            defl = np.array(
                [
                    (
                        self.alpha_in(x_[i], y_[i], kwargs_slice)
                        if (x_rot[i] ** 2 / a**2) + (y_rot[i] ** 2 / b**2) <= 1
                        else self.alpha_ext(x_[i], y_[i], kwargs_slice)
                    )
                    for i in range(len(x_))
                ]
            )
            return defl[:, 0], defl[:, 1]

    def hessian(self, x, y, a, b, psi, sigma_0, center_x=0.0, center_y=0.0):
        """Lensing second derivatives.

        :param a: float, semi-major axis, must be positive
        :param b: float, semi-minor axis, must be positive
        :param psi: float, orientation in radian
        :param sigma_0: float, surface mass density, must be positive
        :param center_x: float, center on the x axis
        :param center_y: float, center on the y axis
        """

        diff = 0.000000001
        alpha_ra, alpha_dec = self.derivatives(
            x, y, a, b, psi, sigma_0, center_x, center_y
        )
        alpha_ra_dx, alpha_dec_dx = self.derivatives(
            x + diff, y, a, b, psi, sigma_0, center_x, center_y
        )
        alpha_ra_dy, alpha_dec_dy = self.derivatives(
            x, y + diff, a, b, psi, sigma_0, center_x, center_y
        )

        f_xx = (alpha_ra_dx - alpha_ra) / diff
        f_xy = (alpha_ra_dy - alpha_ra) / diff
        f_yx = (alpha_dec_dx - alpha_dec) / diff
        f_yy = (alpha_dec_dy - alpha_dec) / diff
        return f_xx, f_xy, f_yx, f_yy

    @staticmethod
    def sign(z):
        """Sign function.

        :param z: complex
        """
        x = z.real
        y = z.imag
        if x > 0 or (x == 0 and y >= 0):
            return 1
        else:
            return -1

    def alpha_in(self, x, y, kwargs_slice):
        """Deflection angle for (x,y) inside the elliptical slice.

        :param kwargs_slice: dict, dictionary with the slice definition
            (a,b,psi,sigma_0)
        """
        z = complex(x, y)
        zb = z.conjugate()
        psi = kwargs_slice["psi"]
        e = (kwargs_slice["a"] - kwargs_slice["b"]) / (
            kwargs_slice["a"] + kwargs_slice["b"]
        )
        sig_0 = kwargs_slice["sigma_0"]
        e2ipsi = cmath.exp(2j * psi)
        I_in = (z - e * zb * e2ipsi) * sig_0
        return I_in.real, I_in.imag

    def alpha_ext(self, x, y, kwargs_slice):
        """Deflection angle for (x,y) outside the elliptical slice.

        :param kwargs_slice: dict, dictionary with the slice definition
            (a,b,psi,sigma_0)
        """
        z = complex(x, y)
        r, phi = param_util.cart2polar(x, y)
        zb = z.conjugate()
        psi = kwargs_slice["psi"]
        a = kwargs_slice["a"]
        b = kwargs_slice["b"]
        f2 = a**2 - b**2
        # c = a * b / f2
        sig_0 = kwargs_slice["sigma_0"]
        median_op = False
        # when (x,y) is on one of the ellipse axis, there might be an issue when calculating the square root of
        # zb ** 2 * e2ipsi - f2. When the argument has an imaginary part ==0, having 0. or -0. may return different
        # answers. Therefore, for points (x,y) close to one axis, we take 3 points (one is x,y ; another one is a delta
        # away from this position, perpendicularly to the axis ; another one is at -delta perpendicularly away from
        # x,y). We calculate the function for each point and take the median. This avoids any singularity for points
        # along the axis but it slows down the function.
        if (
            np.abs(np.sin(phi - psi)) <= 10**-10
            or np.abs(np.sin(phi - psi - np.pi / 2.0)) <= 10**-10
        ):  # very close to one of the ellipse axis
            median_op = True
        e2ipsi = cmath.exp(2j * psi)
        eipsi = cmath.exp(1j * psi)
        if median_op is True:
            eps = 10**-10
            z_minus_eps = complex(r * np.cos(phi - eps), r * np.sin(phi - eps))
            zb_minus_eps = z_minus_eps.conjugate()
            z_plus_eps = complex(r * np.cos(phi + eps), r * np.sin(phi + eps))
            zb_plus_eps = z_plus_eps.conjugate()
            I_out_minus = (
                2
                * a
                * b
                / f2
                * (
                    zb_minus_eps * e2ipsi
                    - eipsi
                    * self.sign(zb_minus_eps * eipsi)
                    * cmath.sqrt(zb_minus_eps**2 * e2ipsi - f2)
                )
                * sig_0
            )
            I_out_plus = (
                2
                * a
                * b
                / f2
                * (
                    zb_plus_eps * e2ipsi
                    - eipsi
                    * self.sign(zb_plus_eps * eipsi)
                    * cmath.sqrt(zb_plus_eps**2 * e2ipsi - f2)
                )
                * sig_0
            )
            I_out_mid = (
                2
                * a
                * b
                / f2
                * (
                    zb * e2ipsi
                    - eipsi * self.sign(zb * eipsi) * cmath.sqrt(zb**2 * e2ipsi - f2)
                )
                * sig_0
            )
            I_out_real = np.median([I_out_minus.real, I_out_plus.real, I_out_mid.real])
            I_out_imag = np.median([I_out_minus.imag, I_out_plus.imag, I_out_mid.imag])
        else:
            if a == b and x**2 + y**2 > a**2:
                # if round, simpler formula is valid
                I_out_real = sig_0 * a**2 * x / (x**2 + y**2)
                I_out_imag = sig_0 * a**2 * y / (x**2 + y**2)

                return I_out_real, I_out_imag
            I_out = (
                2
                * a
                * b
                / f2
                * (
                    zb * e2ipsi
                    - eipsi * self.sign(zb * eipsi) * cmath.sqrt(zb**2 * e2ipsi - f2)
                )
                * sig_0
            )

            I_out_real = I_out.real
            I_out_imag = I_out.imag

        # buf = zb ** 2 * e2ipsi - f2  ##problem with 0. and -0. giving different answers
        # if buf.real == 0:
        #     buf = complex(0, buf.imag)
        # if buf.imag == 0:
        #     buf = complex(buf.real, 0)

        return I_out_real, I_out_imag

    @staticmethod
    def pot_in(x, y, kwargs_slice):
        """Lensing potential for (x,y) inside the elliptical slice.

        :param kwargs_slice: dict, dictionary with the slice definition
            (a,b,psi,sigma_0)
        """
        psi = kwargs_slice["psi"]
        a = kwargs_slice["a"]
        b = kwargs_slice["b"]
        sig_0 = kwargs_slice["sigma_0"]
        e = (a - b) / (a + b)
        rE = (a + b) / 2.0
        pot_in = (
            0.5
            * (
                (1 - e) * (x * np.cos(psi) + y * np.sin(psi)) ** 2
                + (1 + e) * (y * np.cos(psi) - x * np.sin(psi)) ** 2
            )
            * sig_0
        )
        cst = sig_0 * rE**2 * (1 - e**2) * np.log(rE)
        return pot_in + cst

    def pot_ext(self, x, y, kwargs_slice):
        """Lensing potential for (x,y) outside the elliptical slice.

        :param kwargs_slice: dict, dictionary with the slice definition
            (a,b,psi,sigma_0)
        """
        z = complex(x, y)
        # zb = z.conjugate()
        psi = kwargs_slice["psi"]
        a = kwargs_slice["a"]
        b = kwargs_slice["b"]
        sig_0 = kwargs_slice["sigma_0"]
        r, phi = param_util.cart2polar(x, y)
        median_op = False
        # when (x,y) is on one of the ellipse axis, there might be an issue when calculating the square root of
        # z ** 2 * em2ipsi - f2. When the argument has an imaginary part ==0, having 0. or -0. may return different
        # answers. Therefore, for points (x,y) close to one axis, we take 3 points (one is x,y ; another one is a delta
        # away from this position, perpendicularly to the axis ; another one is at -delta perpendicularly away from
        # x,y). We calculate the function for each point and take the median. This avoids any singularity for points
        # along the axis but it slows down the function.
        if (
            np.abs(np.sin(phi - psi)) <= 10**-10
            or np.abs(np.sin(phi - psi - np.pi / 2.0)) <= 10**-10
        ):  # very close to one of the ellipse axis
            median_op = True
        e = (a - b) / (a + b)
        f2 = a**2 - b**2
        emipsi = cmath.exp(-1j * psi)
        em2ipsi = cmath.exp(-2j * psi)
        if median_op is True:
            eps = 10**-10
            z_minus_eps = complex(r * np.cos(phi - eps), r * np.sin(phi - eps))
            z_plus_eps = complex(r * np.cos(phi + eps), r * np.sin(phi + eps))

            pot_ext_minus = (
                (1 - e**2)
                / (4 * e)
                * (
                    f2
                    * cmath.log(
                        (
                            self.sign(z_minus_eps * emipsi) * z_minus_eps * emipsi
                            + cmath.sqrt(z_minus_eps**2 * em2ipsi - f2)
                        )
                        / 2.0
                    )
                    - self.sign(z_minus_eps * emipsi)
                    * z_minus_eps
                    * emipsi
                    * cmath.sqrt(z_minus_eps**2 * em2ipsi - f2)
                    + z_minus_eps**2 * em2ipsi
                )
                * sig_0
            )
            pot_ext_plus = (
                (1 - e**2)
                / (4 * e)
                * (
                    f2
                    * cmath.log(
                        (
                            self.sign(z_plus_eps * emipsi) * z_plus_eps * emipsi
                            + cmath.sqrt(z_plus_eps**2 * em2ipsi - f2)
                        )
                        / 2.0
                    )
                    - self.sign(z_plus_eps * emipsi)
                    * z_plus_eps
                    * emipsi
                    * cmath.sqrt(z_plus_eps**2 * em2ipsi - f2)
                    + z_plus_eps**2 * em2ipsi
                )
                * sig_0
            )
            pot_ext_mid = (
                (1 - e**2)
                / (4 * e)
                * (
                    f2
                    * cmath.log(
                        (
                            self.sign(z * emipsi) * z * emipsi
                            + cmath.sqrt(z**2 * em2ipsi - f2)
                        )
                        / 2.0
                    )
                    - self.sign(z * emipsi)
                    * z
                    * emipsi
                    * cmath.sqrt(z**2 * em2ipsi - f2)
                    + z**2 * em2ipsi
                )
                * sig_0
            )
            pot_ext = np.median(
                [pot_ext_minus.real, pot_ext_plus.real, pot_ext_mid.real]
            )
        else:
            pot_ext = (
                (1 - e**2)
                / (4 * e)
                * (
                    f2
                    * cmath.log(
                        (
                            self.sign(z * emipsi) * z * emipsi
                            + cmath.sqrt(z**2 * em2ipsi - f2)
                        )
                        / 2.0
                    )
                    - self.sign(z * emipsi)
                    * z
                    * emipsi
                    * cmath.sqrt(z**2 * em2ipsi - f2)
                    + z**2 * em2ipsi
                )
                * sig_0
            ).real
        return pot_ext

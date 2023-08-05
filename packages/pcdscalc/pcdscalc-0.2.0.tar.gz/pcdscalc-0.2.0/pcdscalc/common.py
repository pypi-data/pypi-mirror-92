"""Module that holds common calculations."""
import numpy as np
from .constants import WAVELENGTH_TO_ENERGY_LAMBDA, units


def cosd(angle):
    """
    Cos of an angle specified in degrees.

    Parameters
    ----------
    angle : number
        Angle in degrees.

    Returns
    -------
    arad : number
        The corresponding cosine value of `angle` input.
    """
    arad = np.deg2rad(angle)
    return np.cos(arad)


def sind(angle):
    """
    Sin of an angle specified in degrees.

    Parameters
    ----------
    angle : number
        Angle in degrees.

    Returns
    -------
    arad : number
        The corresponding sine value of `angle` input.
    """
    arad = np.deg2rad(angle)
    return np.sin(arad)


def tand(angle):
    """
    Tan of an angle specified in degrees.

    Parameters
    ----------
    angle : number
        Angle in degrees.

    Returns
    -------
    arad : number
        The corresponding tangent value of `angle` input.
    """
    arad = np.deg2rad(angle)
    return np.tan(arad)


def asind(x):
    """
    Arcsin in degrees. Closed interval of [-pi/2, pi/2].

    Parameters
    ----------
    x : number
        y-coordinate on the unit circle.

    Returns
    -------
    arad : number
        The inverse sine of x in degrees.
    """
    angle = np.arcsin(x)
    return np.rad2deg(angle)


def acosd(x):
    """
    Arccos in degrees.

    Parameters
    ----------
    x : number
        x-coordinate on the unit circle.
        For real arguments the domain is [-1, 1].

    Returns
    -------
    arad : number
        The angle of the ray intersecting the unit circle at the given
        x-coordinate in degrees.
    """
    angle = np.arccos(x)
    return np.rad2deg(angle)


def atand(x):
    """
    Arctan in degrees.

    Parameters
    ----------
    x : number

    Returns
    -------
    arad : number
        Has the same shape as x. Its real part is in [-pi/2, pi/2]
        (arctan(+/-inf) returns +/-pi/2).
    """
    angle = np.arctan(x)
    return np.rad2deg(angle)


def energy_to_wavelength(energy):
    """
    Compute photon wavelength in m.

    Parameters
    ----------
    energy : number
        Photon energy in eV.

    Returns
    -------
    wavelength : float
        Wavelength [m].
    """
    return (WAVELENGTH_TO_ENERGY_LAMBDA / energy) / units["ang"]


def wavelength_to_energy(wavelength):
    """
    Compute photon energy in eV.

    Parameters
    ----------
    wavelength : number
        The photon wavelength in m.

    Returns
    -------
    energy : number
        Photon Energy in eV.
    """
    return WAVELENGTH_TO_ENERGY_LAMBDA / (wavelength * units["ang"])

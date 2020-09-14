import numpy as np

def check_contours(contour):
    """Check that contour is an array of two vectors for x and y
    Args:
        contour [array-like]: array like `np.array([[x], [y]])`
    Return:
        contour [array-like]: array like `np.array([[x], [y]])`
    """
    try:
        assert contour.shape[1] > 0
    except IndexError:
        raise IndexError('contour must be an array of `.shape` (2,n)')
    try:
        assert contour.shape[0] == 2
    except AssertionError:
        raise AssertionError('contour must have `.shape` (2,n)')
    return contour

def calc_grv(thickness, height, area, top='slab', g=False):
    """Calculate GRV for given prospect
    Args:
        thickness [float]: average thickness of reservoir
        height [float]: height of hydrocarbon column
        area [float]: area of hydrocarbon prospect
        top: structure shape, one of `{'slab', 'round', 'flat'}`
        g [float]: geometric correction factor
    Returns:
        grv following `thickness * area * geometric_correction_factor`
    """
    if g:
        g = g
    else:
        ratio = thickness / height

        if top == 'round':
            g = -0.6 * ratio + 1
        elif top == 'flat':
            g = -0.3 * ratio + 1
        else:
            g = 1
    return thickness * area * g, g


def calc_hciip(GRV, phi=1, NTG=1, Sw=0, FVF=1, fluid='oil'):
    """Calculate Hydrocarbon initially in-place for a given prospect
    Args:
        GRV [float]: gross rock volume [acre-feet]
        phi [float]: porosity [fraction]
        NTG [float]: net-to-gross [fraction]
        Sw [float]: water saturation [fraction]
        FVF [float]: formation volume factor (Bo for oil or Bg for gas) [RES bbl/STB or RES ft3/SCF]
    Return:
        HCIIP [float]: according to `(constant * GRV * phi * NTG * (1 - Sw)) / FVF` with
        a `constant` of 7758 for oil and 43560 for gas
    """

    try:
        if fluid.lower() not in {'oil', 'gas'}:
            raise ValueError("`fluid` arg must be of `{'gas', 'oil'}`")
    except AttributeError:
        raise AttributeError("`fluid` arg must be of type `str`")

    if fluid == 'oil':
        constant = 7758 # conversion factor from acre-ft to bbl
    elif fluid == 'gas':
        constant = 43560 # conversion factor from acre-ft to ft3

    return (constant * GRV * phi * NTG * (1 - Sw)) / FVF


def poly_area(x,y):
    """Implementation of Shoelace formula
    Args:
        x, y: coordinate vectors [array-like]
        Coordinate vectors *MUST BE* provided in an ordered (clockwise/counter clockwise) manner
    Return:
        area: [float]
    References:
        https://en.wikipedia.org/wiki/Shoelace_formula
        https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
    """
    return 0.5 * np.abs(np.dot(x, np.roll(y,1)) - np.dot(y, np.roll(x,1)))


def calc_areas_from_countour_set(*contour_sets):
    """Calculate poly_area for each contour
    Args:
        contour_sets: contours, positional args of type `np.array([[...],[...]]`
    Returns:
        areas: array of areas
        contour_set: tuple of inputs
    """
    areas = np.array([poly_area(c[0], c[1]) for c in np.array(contour_sets)])
    #print(f'areas.shape: {areas.shape}')
    return areas, (contour_sets)


def closest_depths_to_contact(arr, contact):
    """Get closest depths to contact in an array"""
    close_0 = arr.flat[np.abs(arr - contact).argmin()]
    arr2 = arr[arr != close_0]
    close_1 = arr2.flat[np.abs(arr2 - contact).argmin()]
    return close_0, close_1


def closest_areas_to_contact(areas, arr, c0, c1):
    """Get equivalent closest areas to contact"""
    area_0 = areas[np.where(arr == c0)][0]
    area_1 = areas[np.where(arr == c1)][0]
    return area_0, area_1


def last_base_slope(c0, c1, a0, a1):
    """Calculate slope of line"""
    dy = c1 - c0
    dx = a1 - a0
    return dy / dx


def calc_x_for_contact_depth(m, c, contact):
    """Calculate x for contact depth
    Args:
        m: slope from `last_base_slope`
        c: intercept from `c0`
    """
    return 1 / m * (contact - c)


def calc_x_actual(x, a0):
    """Calculate x position of intersection of base with contact"""
    return x + a0


def get_sq_root(a):
    """Find a square root such that one area is half the other
    Args:
        a: root of larger area
        A: area of larger area
        a_: root of smaller area
        A_: area of smaller area
    Return:
        a, A, a_, A_
    """
    A = a**2
    a_ = np.sqrt(A / 2)
    A_ = a_**2
    return a, A, a_, A_
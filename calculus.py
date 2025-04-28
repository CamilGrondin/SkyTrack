import math

from datetime import datetime

def floor(x: float) -> int:
    """
    Returns the greatest integer value k such that k <= x.

    Example:
        floor(3.6)  ->  3
        floor(-3.6) -> -4
    """
    return math.floor(x)


def cprNL(lat: float) -> int:
    """NL() function in CPR decoding.

    Args:
        lat (float): Latitude in degrees.

    Returns:
        int: Number of latitude zones (NL).
    """

    if math.isclose(lat, 0, abs_tol=1e-6):  # Tolérance pour la comparaison avec 0
        return 59
    elif math.isclose(abs(lat), 87, abs_tol=1e-6):
        return 2
    elif abs(lat) > 87:
        return 1

    nz = 15
    a = 1 - math.cos(math.pi / (2 * nz))
    b = math.cos(math.radians(abs(lat))) ** 2  # math.radians(x) = x * pi / 180
    nl = 2 * math.pi / (math.acos(1 - a / b))

    return math.floor(nl)

def decode_cpr(lat_cpr_even, lat_cpr_odd, lon_cpr_even, lon_cpr_odd):
    """Decode airborne position from a pair of even and odd position message

    Args:
        msg0 (string): even message (28 hexdigits)
        msg1 (string): odd message (28 hexdigits)
        t0 (int): timestamps for the even message
        t1 (int): timestamps for the odd message

    Returns:
        (float, float): (latitude, longitude) of the aircraft
    """



    # 131072 is 2^17, since CPR lat and lon are 17 bits each.
    cprlat_even = lat_cpr_even / 131072
    cprlon_even = lon_cpr_even / 131072
    cprlat_odd = lat_cpr_odd / 131072
    cprlon_odd = lon_cpr_odd / 131072

    air_d_lat_even = 360 / 60
    air_d_lat_odd = 360 / 59

    # compute latitude index 'j'
    j = floor(59 * cprlat_even - 60 * cprlat_odd + 0.5)

    lat_even = float(air_d_lat_even * (j % 60 + cprlat_even))
    lat_odd = float(air_d_lat_odd * (j % 59 + cprlat_odd))

    if lat_even >= 270:
        lat_even = lat_even - 360

    if lat_odd >= 270:
        lat_odd = lat_odd - 360

    # check if both are in the same latidude zone, exit if not
    if cprNL(lat_even) != cprNL(lat_odd):
        return None

    # compute ni, longitude index m, and longitude
    # (people pass int+int or datetime+datetime)

    lat = lat_odd
    nl = cprNL(lat)
    ni = max(cprNL(lat) - 1, 1)
    m = floor(cprlon_even * (nl - 1) - cprlon_odd * nl + 0.5)
    lon = (360 / ni) * (m % ni + cprlon_odd)

    if lon > 180:
        lon = lon - 360

    return lat, lon


# 🔹 Tes valeurs d'entrée (extraites d'un message ADS-B)
lat_cpr_even = 93000
lat_cpr_odd = 74158
lon_cpr_even = 51372
lon_cpr_odd = 50194

latitude, longitude = decode_cpr(lat_cpr_even, lat_cpr_odd, lon_cpr_even, lon_cpr_odd)

if latitude is not None and longitude is not None:
    print(f"Latitude: {latitude:.6f}, Longitude: {longitude:.6f}")
else:
    print("Erreur : les données CPR sont incohérentes.")
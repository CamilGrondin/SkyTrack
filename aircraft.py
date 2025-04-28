class Aircraft:
    def __init__(self, oaci, callsign, latitude, longitude, altitude,lat_cpr_even=0, lat_cpr_odd=0, long_cpr_even=0, long_cpr_odd=0):
        self.oaci = oaci
        self.callsign = callsign
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.lat_cpr_even = lat_cpr_even
        self.lat_cpr_odd = lat_cpr_odd
        self.long_cpr_even = long_cpr_even
        self.long_cpr_odd = long_cpr_odd


    def __repr__(self):
        return f"Aircraft({self.oaci}, {self.callsign}, {self.latitude}, {self.longitude}, {self.altitude}, {self.lat_cpr_even}, {self.lat_cpr_odd}, {self.long_cpr_even}, {self.long_cpr_odd})"

#
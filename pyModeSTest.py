"""
import pyModeS as pms

pms.tell("8D4840D6202CC371C32CE0576098")
"""

import pyModeS as pms

msg0 = "8d4b161248bf309ab290b54d556e"
msg1 = "8d4b1612485f6c03b0932a6f2d27"
t0 = 1457996402
t1 = 1457996400

print(pms.tell(msg0))
print(pms.tell(msg1))

print(pms.adsb.position(msg0, msg1, t0, t1))
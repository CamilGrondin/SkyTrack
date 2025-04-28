import socket
import re
from typing import Any
import math
import pyModeS as pms

from aircraft import Aircraft
from calculus import decode_cpr
PORT = 5005  # Doit être le même que sur le serveur
aircrafts = {}


def extract_bits_message(hex_string, start_bit, end_bit):
    binary_string = bin(int(hex_string, 16))[2:].zfill(112)
    extracted_bits = binary_string[start_bit - 1:end_bit]
    hex_result = hex(int(extracted_bits, 2))[2:].upper().zfill(
        (end_bit - start_bit + 3) // 4)
    return hex_result

def extrat_oaci_from_hex(tramehex):
    oaci = tramehex[2:8]
    #print(f"oaci : {oaci}")
    return oaci

def extract_bits_decimal(hex_message, start_bit, end_bit):
    binary_message = bin(int(hex_message, 16))[2:].zfill(112)
    extracted_bits = binary_message[start_bit:end_bit+1]
    return int(extracted_bits, 2)

def decode_callsign(callsign_bits):
    mapping = {
        **{i: chr(64 + i) for i in range(1, 27)},  # A-Z (1-26)
        **{i: chr(i) for i in range(48, 58)},  # 0-9 (48-57)
        32: ' '  # Espace (32)
    }
    return "".join(mapping.get(bit, "") for bit in callsign_bits)

def process_frame(hex_frame):
    extracted = extract_bits_message(hex_frame, 33, 88)
    valeur_entiere_message_payload = int(extracted, 16)
    first_5_bits_tc = (valeur_entiere_message_payload >> (56 - 5)) & 0b11111

    if 1 <= first_5_bits_tc <= 4:
        callsign_bits = [(valeur_entiere_message_payload >> (6 * (7 - i))) & 0b111111 for i in range(8)]
        decoded_callsign = decode_callsign(callsign_bits)
        print(f"Callsign décodé : {decoded_callsign}")
        if aircrafts.get(extrat_oaci_from_hex(hex_frame)):
            aircraft_id = aircrafts.get(extrat_oaci_from_hex(hex_frame))
            aircraft_id.callsign = decoded_callsign
        else:
            aircrafts[extrat_oaci_from_hex(hex_frame)] = Aircraft(extrat_oaci_from_hex(hex_frame), "", 0.0, 0.0, 0)



#ICI ON EST DANS LE CAS DU CALCUL DE POSITION
    elif (9 <= first_5_bits_tc <= 18) or (20 <= first_5_bits_tc <= 22):
        if aircrafts.get(extrat_oaci_from_hex(hex_frame)):
            aircraft_pos = aircrafts.get(extrat_oaci_from_hex(hex_frame))
            value_flag =  bit_cpr_flag = (valeur_entiere_message_payload >> (56 - 22)) & 0x1
            latitude = extract_bits_decimal(hex_frame, 55, 71)
            longitude = extract_bits_decimal(hex_frame, 72, 88)
            if value_flag == 0:
                aircraft_pos.lat_cpr_even = latitude
                aircraft_pos.long_cpr_even = longitude
            elif aircraft_pos.lat_cpr_even != 0 and aircraft_pos.long_cpr_even != 0:
                print(f"OACI FLAG 1 : {extrat_oaci_from_hex(hex_frame)}")
                print(aircraft_pos)
                aircraft_pos.lat_cpr_odd = latitude
                aircraft_pos.long_cpr_odd = longitude
                print(f"aircraft : {aircraft_pos}")
                lat, long = decode_cpr(aircraft_pos.lat_cpr_even, aircraft_pos.lat_cpr_odd, aircraft_pos.long_cpr_even, aircraft_pos.long_cpr_odd)
                if lat is not None and long is not None:
                    print(f"Latitude: {lat:.6f}, Longitude: {long:.6f}")
                    aircraft_pos.latitude = lat
                    aircraft_pos.longitude = long
                else:
                    print("Erreur : les données CPR sont incohérentes.")
                aircraft_pos.lat_cpr_even=0
                aircraft_pos.long_cpr_even=0
                aircraft_pos.lat_cpr_odd=0
                aircraft_pos.long_cpr_odd=0
        #print(aircraft_pos)

    return None

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

print(f"Écoute des données sur le port {PORT}...")


try:
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        adsb_hexa = re.search(r'\*([a-fA-F0-9]+);', message)
        trame_hex =  adsb_hexa.group(1)
        if not pms.crc(trame_hex):
            print(trame_hex)
            if trame_hex.upper().startswith('8D'):
                oaci = extrat_oaci_from_hex(trame_hex)
                if oaci not in aircrafts:
                    aircrafts[oaci] = Aircraft(oaci, "", 0.0, 0.0, 0)
                #print(aircrafts)
                process_frame(trame_hex)
except KeyboardInterrupt:
    print("\nArrêt du client.")
finally:
    sock.close()
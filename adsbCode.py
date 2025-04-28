from math import floor, pi, acos, cos
from random import randint
import time
import json
import folium
from IPython.display import display
import threading

HEX = ""
HEX_ARRAY = []
# d434040844e44118c00048355c94

def afficher_carte(lat, lon, carte=None, speed="", ground_track="", altitude="", surveillance_status="", single_antenna_flag="", decoded_altitude=0, icao=""):
    # Si aucune carte n'est fournie, en créer une nouvelle centrée sur les coordonnées actuelles
    if carte is None:
        carte = folium.Map(location=[lat, lon], zoom_start=12, tiles="cartodbpositron")
        
    # Ajout d'un marqueur à la carte existante
    popup_content = "<br>".join(filter(None, [
        f"Vitesse: <span style='color:blue;'>{speed} kt</span>" if speed else None,
        f"Cap au sol: <span style='color:blue;'>{ground_track}°</span>" if ground_track else None,
        f"Altitude: <span style='color:blue;'>{altitude}</span>" if altitude else None,
        f"Surveillance: <span style='color:blue;'>{surveillance_status}</span>" if surveillance_status else None,
        f"Antennes: <span style='color:blue;'>{single_antenna_flag}</span>" if single_antenna_flag else None,
        f"Altitude décodée: <span style='color:blue;'>{decoded_altitude} ft</span>" if decoded_altitude else None
    ]))

    folium.Marker(
        location=[lat, lon],
        popup=popup_content,
        tooltip="Position de l'avion",
        icon=folium.CustomIcon("plane.png", icon_size=(30, 30))
    ).add_to(carte)

    if icao:
        folium.Marker(
            location=[lat + 0.001, lon + 0.001],  # Slight offset to position the label near the marker
            icon=folium.DivIcon(html=f"<div style='font-size: 12px; color: black; background-color: yellow; padding: 2px; border-radius: 3px; white-space: nowrap;'>{icao}</div>")
        ).add_to(carte)

    # Sauvegarde de la carte dans un fichier HTML
    carte.save("carte.html")

    return carte

aircrafts = []
def print_aircrafts():
    carte = None
    while True:
        print("Aircrafts:", aircrafts)
        for aircraft in aircrafts:
            print(f"ICAO: {aircraft.icao}, Callsign: {aircraft.callsign}, Position: {aircraft.position}")
            if aircraft.position is not None:
                carte = afficher_carte(aircraft.position[0], aircraft.position[1], carte, aircraft.speed, aircraft.ground_track, aircraft.altitude, aircraft.surveillance_status, aircraft.single_antenna_flag, aircraft.decoded_altitude, aircraft.callsign)
            else:
                random_lon = randint(-180, 180)
                carte = afficher_carte(0, random_lon, carte, aircraft.speed, aircraft.ground_track, aircraft.altitude, aircraft.surveillance_status, aircraft.single_antenna_flag, aircraft.decoded_altitude, aircraft.icao)
        time.sleep(10)

# Start the thread to print aircrafts every 10 seconds
thread = threading.Thread(target=print_aircrafts, daemon=True)
thread.start()

class Aircraft:
    def __init__(self, icao, callsign=None):
        self.icao = icao
        self.callsign = callsign
        self.position = None
        self.speed = None
        self.ground_track = None
        self.altitude = None
        self.surveillance_status = None
        self.single_antenna_flag = None
        self.decoded_altitude = None

    def __repr__(self):
        return f"Aircraft(icao='{self.icao}', callsign='{self.callsign}')"

def NL(lat):
    try:
        return floor(2 * pi / acos(1 - (1 - cos(pi / (2 * 15))) / (cos((pi / 180) * lat))**2))
    except ValueError:
        return 1  # Return a default value in case of math domain error

try:
    def decript_position(enc_lat_even, enc_lon_even, enc_lat_odd, enc_lon_odd, type):
        lat_cpr_even = enc_lat_even / 2**17
        lon_cpr_even = enc_lon_even / 2**17
        lat_cpr_odd = enc_lat_odd / 2**17
        lon_cpr_odd = enc_lon_odd / 2**17
        
        j = floor(59 * lat_cpr_even - 60 * (lat_cpr_odd) + 0.5)
        
        lat_even = (type / (4 * 15)) * ((j % 60) + lat_cpr_even)
        lat_odd = (type / (4 * 15 - 1)) * ((j % 59) + lat_cpr_odd)
        
        NL_lat_even = NL(lat_even)
        NL_lat_odd = NL(lat_odd)
        
        if(NL_lat_even == NL_lat_odd):
            lat = lat_even
        else:
            print("---")
            print("The pair of messages are from different longitude zones, and it is not possible to compute the correct global position.")
            print("---")
            return 0, 0  # Return default values to avoid referencing uninitialized variables
        
        m = floor(lon_cpr_even * (NL_lat_even - 1) - lon_cpr_odd * NL_lat_even + 0.5)
        
        n = max(NL_lat_even, 0.1)
        
        lon = (360 / n) * (m % n + lon_cpr_even)
        
        return lat, lon
    
    with open("./data.json", "r") as f:
        HEX_ARRAY = json.load(f)
    carte = None

    for HEX in HEX_ARRAY['data']:
        print("---")
        print("HEX : " + HEX)
        print("---")
        
        BITS = bin(int(HEX, 16))[2:]
        print(BITS)
        DF = BITS[:5]
        print("DF : " + DF)

        CA = BITS[5:8]
        print("CA : " + CA)

        ICAO = BITS[8:32]
        print("ICAO : " + ICAO)

        TC = BITS[32:37]
        print("TC : " + TC)

        ME = BITS[32:88]
        print("ME : " + ME)

        PI = BITS[89:112]
        print("PI : " + PI)

        print("---")

        MAP = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ##### ###############0123456789######"

        ref_lat = 51.990
        ref_lon = 4.375

        # Constants
        Nz = 15

        def NL(lat):
            try:
                return floor(2 * pi / acos(1 - (1 - cos(pi / (2 * Nz))) / (cos((pi / 180) * lat))**2))
            except ValueError:
                return 1


        if(DF == "10001" or DF == "10010"):
            print("DF = 17")
            
            if(CA == "101"):
                print("CA = 5")

            print("ICAO : " + HEX[2:8])
            
            if(int(TC, 2) <= 4):
                print("TC = Aircraft identification")

                if(int(TC, 2) == 4):
                    if(int(CA, 2) == 1):
                        print("Light (less than 7000 kg)")
                    
                    if(int(CA, 2) == 2):
                        print("Medium 1 (between 7000 kg and 34000 kg)")
                        
                    if(int(CA, 2) == 3):
                        print("Medium 2 (between 34000 kg to 136000 kg)")
                        
                    if(int(CA, 2) == 4):
                        print("High vortex aircraft")
                    
                    if(int(CA, 2) == 5):
                        print("Heavy aircraft")
                    
                    if(int(CA, 2) == 6):
                        print("High performance (>5 g acceleration) and high speed (>400 kt)")
                    
                    if(int(CA, 2) == 7):
                        print("Rotorcraft")
                    
                    
                    print("Immatriculation : ")
                    callsign = ""
                    for i in range(8, len(ME), 6):
                        char_index = int(ME[i:i+6], 2)
                        callsign += MAP[char_index]
                        print(MAP[char_index], end="")
                        
                    print("callsign1 : " + callsign.strip())
                    aircrafts.append(Aircraft(icao=ICAO, callsign=callsign.strip()))
                    
                elif(int(TC, 2) in {1, 2, 3}):
                    print("Not a plane")
            
            elif(int(TC, 2) <= 8):
                print("TC = Surface position")
                
                if HEX_ARRAY and HEX_ARRAY['data'][-1] == HEX:
                    print("Already received")
                    continue
                    
                # HEX_ARRAY.append(HEX)
                print("HEX ARRAY : " + str(HEX_ARRAY))
                
                filtered_hex = [hex_code for hex_code in HEX_ARRAY['data'] if bin(int(hex_code, 16))[2:].zfill(112)[8:32] == ICAO and bin(int(hex_code, 16))[2:].zfill(112)[32:37] == TC]
                print("filtered : " + str(filtered_hex))
                HEX_even = None
                HEX_odd = None

                if len(filtered_hex) == 2:
                    for hex_code in filtered_hex:
                        msg_bits = bin(int(hex_code, 16))[2:]
                        if msg_bits[53:54] == "0":
                            HEX_even = hex_code
                        elif msg_bits[53:54] == "1":
                            HEX_odd = hex_code

                    if HEX_even and HEX_odd:
                        print("HEX_even: ", HEX_even)
                        print("HEX_odd: ", HEX_odd)
                    else:
                        print("Could not find both even and odd HEX codes.")
                        continue
                else:
                    print("Could not find exactly 2 matching HEX codes in HEX_ARRAY.")
                    continue
                
                speed = ""
                ground_track = ""
                    
                MOV = ME[5:12]
                print("Movement : ", end="")
                print(ME[5:12])
                if(int(MOV, 2) == 0):
                    print("Speed not available")
                    speed = "Speed not available"
                elif(int(MOV, 2) == 1):
                    print("Stopped v < 0.125 kt)")
                    speed = "Stopped v < 0.125 kt"
                elif(2 <= int(MOV, 2) <= 8):
                    print("0.125 ≤ v < 1 kt")
                    speed = "0.125 ≤ v < 1 kt"
                elif(9 <= int(MOV, 2) <= 12):
                    print("1 kt ≤ v < 2 kt")
                    speed = "1 kt ≤ v < 2 kt"
                elif(13 <= int(MOV, 2) <= 38):
                    print("2 kt ≤ v < 15 kt")
                    speed = "2 kt ≤ v < 15 kt"
                elif(39 <= int(MOV, 2) <= 93):
                    print("15 kt ≤ v < 70 kt")
                    speed = "15 kt ≤ v < 70 kt"
                elif(94 <= int(MOV, 2) <= 108):
                    print("70 kt ≤ v < 100 kt")
                    speed = "70 kt ≤ v < 100 kt"
                elif(109 <= int(MOV, 2) <= 123):
                    print("100 kt ≤ v < 175 kt")
                    speed = "100 kt ≤ v < 175 kt"
                elif(int(MOV, 2) == 124):
                    print("v ≥ 175 kt")
                    speed = "v ≥ 175 kt"
                elif(125 <= int(MOV, 2) <= 127):
                    print("Reserved")

                S = ME[12:13]
                if(int(S, 2) == 0):
                    print("The ground track fields is invalid")
                    ground_track = "The ground track fields is invalid"
                elif(int(S, 2) == 1):
                    n = int(ME[13:20], 2)
                    X = 360 * n / 128
                    print("Ground track : " + str(X) + "°")
                    ground_track = str(X) + "°"
                
                MSG_HEX = HEX_ARRAY['data'][0]
                MSG = bin(int(MSG_HEX, 16))[2:]

                print("Time : ", end="")
                T = ME[20:21]
                print(int(ME[20:21], 2), end=", ")

                print("CPR Format : ", end="")
                F = MSG[53:54]
                if(int(F, 2) == 0):
                    print("even frame")
                elif(int(F, 2) == 1):
                    print("odd frame")
                    print("---")
                    print("Les valeurs de latitude et longitude sont inversées")
                    print("---")
                    continue

                BITS_even = bin(int(HEX_even, 16))[2:].zfill(112)
                BITS_odd = bin(int(HEX_odd, 16))[2:].zfill(112)
                
                lat_cpr_enc_even = int(BITS_even[54:71], 2)
                print("lat_cpr_enc_even : " + str(lat_cpr_enc_even))
                lat_cpr_enc_odd = int(BITS_odd[54:71], 2)
                print("lat_cpr_enc_odd : " + str(lat_cpr_enc_odd))
                lon_cpr_enc_even = int(BITS_even[71:88], 2)
                print("lon_cpr_enc_even : " + str(lon_cpr_enc_even))
                lon_cpr_enc_odd = int(BITS_odd[71:88], 2)
                print("lon_cpr_enc_odd : " + str(lon_cpr_enc_odd))
                
                position = decript_position(lat_cpr_enc_even, lon_cpr_enc_even, lat_cpr_enc_odd, lon_cpr_enc_odd, 90)
                
                print(" ")
                print("Latitude : ", end="")
                print(round(position[0], 6), end=" N")
                print(" ")
                print("Longitude : ", end="")
                print(round(position[1], 6), end=" E")
                print(f"popup_content : speed={speed}, ground_track={ground_track}")

                # Find the callsign for the given ICAO from the aircrafts list
                callsign = next((aircraft.callsign for aircraft in aircrafts if aircraft.icao == ICAO), None)
                print("callsign : ", callsign)
                
                # Update the position attribute of the aircraft in the list
                for aircraft in aircrafts:
                    if aircraft.icao == ICAO:
                        aircraft.position = (round(position[0], 6), round(position[1], 6))
                        aircraft.speed = speed
                        aircraft.ground_track = ground_track
                        break
                    
                # carte = afficher_carte(round(position[0], 6), round(position[1], 6), carte, speed, ground_track, None, None, None, None, callsign)
            
            elif(int(TC, 2) == 19):
                print("TC = Airborne velocity")
                
                HEX = '8D485020994409940838175B284F'
                HEX2 = '8DA05F219B06B6AF189400CBC33F'
            
            if(int(TC, 2) <= 22):
                print(" ")
                print("TC = Airborne position")
                
                if HEX_ARRAY and HEX_ARRAY['data'][-1] == HEX:
                    print("Already received")
                    continue
                    
                # HEX_ARRAY.append(HEX)
                # print("HEX ARRAY : " + str(HEX_ARRAY))
                
                # Filter HEX_ARRAY to get 2 hex that match the ICAO (BITS[8:32])
                filtered_hex = [hex_code for hex_code in HEX_ARRAY['data'] if bin(int(hex_code, 16))[2:].zfill(112)[8:32] == ICAO and bin(int(hex_code, 16))[2:].zfill(112)[32:37] == TC]
                    
                HEX_even = None
                HEX_odd = None

                if len(filtered_hex) == 2:
                    print("filtered : " + str(filtered_hex))
                    for hex_code in filtered_hex:
                        msg_bits = bin(int(hex_code, 16))[2:]
                        if msg_bits[53:54] == "0":
                            HEX_even = hex_code
                        elif msg_bits[53:54] == "1":
                            HEX_odd = hex_code

                    if HEX_even and HEX_odd:
                        print("HEX_even: ", HEX_even)
                        print("HEX_odd: ", HEX_odd)
                    else:
                        print("Could not find both even and odd HEX codes.")
                        continue
                else:
                    print("Could not find exactly 2 matching HEX codes in HEX_ARRAY.")
                    continue
                
                altitude = ""
                surveillance_status = ""
                single_antenna_flag = ""
                decoded_altitude = 0
                
                print("Altitude : ", end="")
                if(9 <= int(TC, 2) <= 19):
                    print("with barometric altitude")
                    altitude = "with barometric altitude"
                elif(20 <= int(TC, 2) <= 22):
                    print("with GNSS altitude")
                    altitude = "with GNSS altitude"

                print("Surveillance status : ", end="")
                if(int(ME[8:10], 2) == 0):
                    print("No condition")
                    surveillance_status = "No condition"
                elif(int(ME[8:10], 2) == 1):
                    print("Permanent alert")
                    surveillance_status = "Permanent alert"
                elif(int(ME[8:10], 2) == 2):
                    print("Temporary alert")
                    surveillance_status = "Temporary alert"
                elif(int(ME[8:10], 2) == 3):
                    print("Emergency alert")
                    surveillance_status = "Emergency alert"

                print("Single antenna flag : ", end="")
                print(int(ME[10:11], 2))

                print("Encoded altitude : ", end="")
                print(int(ME[11:27], 2))
                decoded_altitude = int(ME[11:27], 2)

                print("Time : ", end="")
                print(int(ME[27:28], 2))

                print("CPR Format : ", end="")
                is_odd = ME[28:29]
                if(int(ME[28:29], 2) == 0):
                    print("even frame")
                elif(int(ME[28:29], 2) == 1):
                    print("odd frame")
                    
                BITS_even = bin(int(HEX_even, 16))[2:].zfill(112)
                BITS_odd = bin(int(HEX_odd, 16))[2:].zfill(112)
                
                lat_cpr_enc_even = int(BITS_even[54:71], 2)
                lat_cpr_enc_odd = int(BITS_odd[54:71], 2)
                lon_cpr_enc_even = int(BITS_even[71:88], 2)
                lon_cpr_enc_odd = int(BITS_odd[71:88], 2)
                
                position = decript_position(lat_cpr_enc_even, lon_cpr_enc_even, lat_cpr_enc_odd, lon_cpr_enc_odd, 360)
                
                print(" ")
                print("Latitude : ", end="")
                print(round(position[0], 6), end=" N")
                print(" ")
                print("Longitude : ", end="")
                print(round(position[1], 6), end=" E")
                print(f"popup_content : altitude={altitude}, surveillance_status={surveillance_status}, single_antenna_flag={single_antenna_flag}, decoded_altitude={decoded_altitude}")

                # Update the position attribute of the aircraft in the list
                for aircraft in aircrafts:
                    if aircraft.icao == ICAO:
                        aircraft.position = (round(position[0], 6), round(position[1], 6))
                        aircraft.altitude = altitude
                        aircraft.surveillance_status = surveillance_status
                        aircraft.single_antenna_flag = single_antenna_flag
                        aircraft.decoded_altitude = decoded_altitude
                        break
                    
                callsign = next((aircraft.callsign for aircraft in aircrafts if aircraft.icao == ICAO), None)
                print("callsign : ", callsign)
                # carte = afficher_carte(round(position[0], 6), round(position[1], 6), carte, None, None, altitude, surveillance_status, single_antenna_flag, decoded_altitude, callsign)
            
            elif(int(TC, 2) == 28):
                print("TC = Aircraft status")
            elif(int(TC, 2) == 29):
                print("TC = Target states and status")
                
            elif(int(TC, 2) == 31):
                print("TC = Operational status")
                
                ST = ME[5:8]
                
                if(int(ST, 2) == 0):
                    print("")
                    print("Aircraft operational status (Version 0)")
                    
                    print("")
                    
                    print("Enroute operational capabilities : ", end="")
                    print(int(ME[8:12]))
                    
                    print("Terminal area operational capabilities : ", end="")
                    print(int(ME[12:16]))
                    
                    print("Approach/landing operational capabilities  : ", end="")
                    print(int(ME[16:20]))
                    
                    print("Surface operational capabilities : ", end="")
                    print(int(ME[20:24]))
                    
                    print("")
                    
                    print("Enroute operational status : ", end="")
                    print(int(ME[24:28]))
                    
                    print("Terminal area operational status : ", end="")
                    print(int(ME[28:32]))
                    
                    print("Approach/landing operational status : ", end="")
                    print(int(ME[32:36]))
                    
                    print("Surface operational status : ", end="")
                    print(int(ME[36:40]))
            
        else:
            print("Not an aircraft")

        print("")
        print("")
        # time.sleep(0.5)
except KeyboardInterrupt:
    print("\nArrêt du client.")

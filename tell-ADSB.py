import json
import pyModeS as pms
import folium
from PIL import Image

HEX_ARRAY = []
Aircarfts = []
aircraft_positions = {}

with open("./data.json", "r") as f:
    HEX_ARRAY = json.load(f)

# Créez une carte centrée sur la position de l'avion
map = folium.Map(location=[48.977205, 2.37561], zoom_start=10)

def afficher_line(aircraft, lat, lon, speed=None):
    """
    Affiche la position de l'avion sur la carte.
    """
    
    # Dessinez une ligne pour suivre la trajectoire de l'avion
    if aircraft['icao'] in aircraft_positions:
        positions = aircraft_positions[aircraft['icao']]
        positions.append((lat, lon))
        # print(speed)
        speed = aircraft.get('speed')[0] if isinstance(aircraft.get('speed'), tuple) else aircraft.get('speed')
        color = "green" if speed and speed < 300 else "orange" if speed and speed < 600 else "red"
        
        folium.PolyLine(positions, color=color, weight=2.5, opacity=1).add_to(map)
    else:
        aircraft_positions[aircraft['icao']] = [(lat, lon)]

for (hex) in HEX_ARRAY['data']:
    try:
        icao = pms.adsb.icao(hex)
        tc = pms.typecode(hex)
        
        remainder = pms.crc(hex)
        
        if remainder != 0:
            # print("CRC error : ", remainder)
            # continue
            pass
        
        if 1 <= tc <= 4: # Identification
            callsign = pms.adsb.callsign(hex)
            category = pms.adsb.category(hex)
            
            if not any(aircraft['icao'] == icao for aircraft in Aircarfts):
                Aircarfts.append({"icao": icao, "callsign": callsign, "tc": tc, "ca": category, "lat": None, "lon": None, "speed": None, "altitude": None})
                
                
        if 5 <= tc <= 18 or 20 <= tc <= 22: # Position
            position = pms.adsb.position_with_ref(hex, 48.977205, 2.37561)
            
            if position:
                lat, lon = position
                aircraft = next((a for a in Aircarfts if a['icao'] == icao), None)
                
                if aircraft:
                    aircraft['lat'] = lat
                    aircraft['lon'] = lon
                    
        if 9 <= tc <= 18: # Altitude in feet
            altitude = pms.adsb.altitude(hex)
            if altitude:
                aircraft = next((a for a in Aircarfts if a['icao'] == icao), None)
                if aircraft:
                    aircraft['altitude'] = altitude
        
        if 20 <= tc <= 22: # Altitude in meters
            altitude = pms.adsb.altitude(hex)
            
            if altitude:
                aircraft = next((a for a in Aircarfts if a['icao'] == icao), None)
                if aircraft:
                    aircraft['altitude'] = altitude * 0.3048  # Convert feet to meters
                    
        if 5 <= tc <= 8 or tc == 19: # Speed
            speed = pms.adsb.velocity(hex)
            if speed:
                aircraft = next((a for a in Aircarfts if a['icao'] == icao), None)
                if aircraft:
                    aircraft['speed'] = speed
                    
        
        if aircraft and aircraft['lat'] is not None and aircraft['lon'] is not None:
            afficher_line(aircraft, aircraft['lat'], aircraft['lon'], aircraft.get('speed'))
        
                    
    except Exception as e:
        print("Error: ", e)
        
# Affichez la position de chaque avion sur la carte
for aircraft in Aircarfts:
    if aircraft['lat'] is not None and aircraft['lon'] is not None:
        # Determine the icon based on 'tc' and 'ca' values
        icon = f"sprite_{aircraft['tc']}_{aircraft['ca']}.png" if 1 <= aircraft['ca'] <= 7 else f"sprite_{aircraft['tc']}.png"

        folium.Marker(
            location=[aircraft['lat'], aircraft['lon']],
            tooltip=(
            f"<b>Immatriculation :</b> {aircraft['callsign']}<br>"
            f"<b>Altitude :</b> {aircraft['altitude']} ft<br>"
            f"<b>Vitesse :</b> {aircraft['speed'][0] if isinstance(aircraft['speed'], tuple) and aircraft['speed'][0] is not None else 'Inconnu'} kt"
            ),
            icon=folium.CustomIcon(
            "plane.png", # icon
            icon_size=(50, 50),
            )
        ).add_to(map)
        

# Enregistrez la carte dans un fichier HTML
map.save("carte.html")

print("Carte enregistrée dans carte.html")

# pm2 start tell-ADSB.py --name ADSB --restart-delay 10000
# pm2 start req.py --name serveur --restart-delay 30000

# pm2 logs ADSB
Bien sûr ! Voici ton fichier readme.md réécrit dans une vraie version GitHub professionnelle, avec badges, nom de projet, licence MIT, et liens formatés.

Je te propose ce nouveau contenu pour ton fichier /Users/camilgrondin/Desktop/ESA/ADSB/readme.md :

⸻



# ADS-B Visualizer ✈️

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

**ADS-B Visualizer** est un projet de lecture, décodage et visualisation de messages ADS-B émis par des avions.  
Les données sont extraites d'un fichier JSON, décodées avec `pyModeS`, puis tracées sur une carte interactive générée avec `folium`.

---

## 📡 Fonctionnalités

- 📥 Décodage des trames ADS-B : identification, position, altitude, vitesse.
- 📍 Suivi dynamique de la trajectoire des avions.
- 🎨 Coloration des trajectoires en fonction de la vitesse :
  - 🟢 Vert : < 300 kt
  - 🟠 Orange : entre 300 et 600 kt
  - 🔴 Rouge : > 600 kt
- 🛫 Affichage des positions finales avec une icône personnalisée.
- 🌐 Export de la carte interactive au format HTML (`carte.html`).

---

## 🗂 Organisation du projet

/ADS-B-Visualizer
├── data.json         # Messages ADS-B bruts
├── tell-ADSB.py      # Script principal
├── plane.png         # Icône pour les avions sur la carte
├── carte.html        # Carte générée après exécution
└── readme.md         # Présentation du projet

---

## ⚙️ Installation

1. **Cloner le dépôt** :

```bash
git clone https://github.com/CamilGrondin/SkyTrack
cd adsb-visualizer

	2.	Installer les dépendances :

pip install pymodes folium pillow



⸻

🚀 Utilisation
	1.	Vérifiez que data.json contient vos trames ADS-B.
	2.	Lancez le script :

python tell-ADSB.py

	3.	Ouvrez carte.html dans votre navigateur pour explorer la carte interactive.

⸻

📋 Remarques
	•	Sources de données : Les messages ADS-B doivent être capturés via un récepteur compatible (ex. dongle RTL-SDR) ou récupérés depuis une base de données.
	•	Fichier d’icône : plane.png est requis pour l’affichage des avions sur la carte. Vous pouvez le personnaliser.
	•	Traitement des erreurs : Les trames invalides sont ignorées avec un message d’erreur en console.

⸻

📈 Améliorations futures
	•	🔄 Rafraîchissement en temps réel avec flux continu.
	•	🛬 Filtres par altitude, vitesse, compagnie aérienne.
	•	🛠 Amélioration de l’interface avec plus de détails par avion.

⸻

📄 Licence

Ce projet est sous licence MIT.
Vous êtes libre de l’utiliser, le modifier et le distribuer.
Voir le fichier LICENSE pour plus d’informations.

⸻

✈️ À propos

Projet réalisé dans un but personnel et éducatif pour l’exploration de données aéronautiques.

⸻
Projet : Visualisation des données ADS-B

📡 Description

Ce projet lit, décode et visualise des messages ADS-B émis par des avions. Les messages sont extraits d’un fichier JSON contenant des trames brutes, puis décodés grâce à la bibliothèque pyModeS. Les trajectoires des avions sont tracées sur une carte interactive générée avec folium.

🛠 Fonctionnalités
	•	Décodage des trames ADS-B : identification, position, altitude, vitesse.
	•	Suivi de la trajectoire de chaque avion avec un tracé dynamique.
	•	Coloration des trajectoires en fonction de la vitesse :
	•	🟢 Vert : < 300 kt
	•	🟠 Orange : entre 300 et 600 kt
	•	🔴 Rouge : > 600 kt
	•	Affichage des positions finales avec une icône personnalisée d’avion.
	•	Export de la carte interactive au format HTML.

🗂 Organisation du projet

/ADS-B-Visualizer
├── data.json         # Messages ADS-B bruts
├── tell-ADSB.py      # Script principal de traitement et visualisation
├── plane.png         # Icône pour les avions sur la carte
├── carte.html        # Carte générée (après exécution du script)
└── readme.md         # Présentation du projet

⚙️ Installation
	1.	Cloner le dépôt :

git clone https://github.com/ton-utilisateur/adsb-visualizer.git
cd adsb-visualizer


	2.	Installer les dépendances :

pip install pymodes folium pillow



🚀 Utilisation
	1.	Assurez-vous que le fichier data.json contient vos trames ADS-B.
	2.	Lancez le script :

python tell-ADSB.py


	3.	Ouvrez carte.html dans votre navigateur pour explorer la carte.

⸻

📋 Remarques
	•	Sources de données : Les messages ADS-B doivent être capturés au préalable via un récepteur compatible (comme un dongle RTL-SDR) ou téléchargés à partir d’une base de données.
	•	Fichier d’icône : Un fichier plane.png est nécessaire pour l’affichage des avions. Vous pouvez personnaliser cette icône.
	•	Traitement des erreurs : Si une trame est invalide ou malformée, elle sera ignorée et une erreur sera affichée dans la console.

⸻

📈 Améliorations futures
	•	Rafraîchissement en temps réel avec un flux continu de trames.
	•	Ajout de filtres par altitude, vitesse ou compagnie aérienne.
	•	Amélioration de l’interface avec des informations détaillées par avion.

⸻

✈️ À propos

Projet réalisé pour la visualisation de données aéronautiques dans le cadre d’une application personnelle/éducative.

⸻

Veux-tu aussi que je te propose une version un peu plus “projet GitHub” avec un badge de version, une licence type MIT, etc. ? 🚀
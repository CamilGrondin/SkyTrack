import socket
import pyModeS as pms

PORT = 5005  # Doit être le même que sur le serveur

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))  # Écoute sur toutes les interfaces

print(f"Écoute des données sur le port {PORT}...")

try:
    while True:
        data, addr = sock.recvfrom(1024)  # Taille du buffer
        pms.tell(data.decode()[1:])
        print("---")
except KeyboardInterrupt:
    print("\nArrêt du client.")
finally:
    sock.close()
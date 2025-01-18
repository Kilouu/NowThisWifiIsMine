from src.rogue_ap.networkscanrogue import *


# Choix de l'Interface   
def choix_network_interface():
    try:
        # Liste les interfaces réseau
        result = subprocess.run(['ip', 'link', 'show'], stdout=subprocess.PIPE, text=True)
        output = result.stdout
        
        # Extrait les noms d'interfaces réseau
        interfaces = []
        for line in output.splitlines():
            if line and line[0].isdigit():
                # Le nom de l'interface se trouve après le numéro et le ':'
                interface_name = line.split(':')[1].strip()
                interfaces.append(interface_name)

        # Affiche les interfaces détectées
        print("Choisissez l'interface réseau à utiliser :")
        for i, interface in enumerate(interfaces, start=1):
            print(f"{i}. {interface}")

        # Choix de l'Interface
        while True:
            try:
                choice = int(input("\nEntrez le numéro de l'interface : "))
                if 1 <= choice <= len(interfaces):
                    selected_interface = interfaces[choice - 1]
                    print(f"\n{SUCCESS_COLOR}[SUCCESS] : Interface sélectionnée : {selected_interface}{RESET_COLOR}\n")
                    return selected_interface
                else:
                    print(f"{ERROR_COLOR}[ERROR] : Veuillez entrer un numéro valide.{RESET_COLOR}")
            except ValueError:
                print(f"{ERROR_COLOR}[ERROR] : Veuillez entrer un nombre valide.{RESET_COLOR}")

    except FileNotFoundError:
        print(f"{ERROR_COLOR}[ERROR] : La commande 'ip' n'est pas disponible sur ce système.{RESET_COLOR}")
    except Exception as e:
        print(f"{ERROR_COLOR}[ERROR] : Une erreur s'est produite : {e}{RESET_COLOR}")


# Kill les process en cours
def kill_process():
    try:
        # Exécution de la commande airmon-ng check kill
        subprocess.run(["sudo", "airmon-ng", "check", "kill"], check=True)
        print(f"{SUCCESS_COLOR}[SUCCESS] : Les processus ont été tués avec succès.{RESET_COLOR}")
    except subprocess.CalledProcessError as e:
        print(f"{ERROR_COLOR}[ERROR] : Erreur lors de l'exécution de la commande : {e}{RESET_COLOR}")


# Liste les réseaux wifi disponibles
def lister_reseaux(interface, fichier_base="Capture/resultats", duree=20):
    try:
        create_directories()
        capture_wifi_networks(interface, fichier_base, duree)
        reseaux = read_csv_and_extract_networks(fichier_base)
        bssid, channel, security, essid = display_networks_and_select_target(reseaux)
        clean_capture_directory()
        clean_result_directory()
        return bssid, channel, security, essid
    except Exception as e:
        print(f"{ERROR_COLOR}[ERROR] : Une erreur s'est produite : {e}{RESET_COLOR}")
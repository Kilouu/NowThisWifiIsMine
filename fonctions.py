import subprocess
import json
import pandas as pd
from Utils.networkscan import *
from Utils.save_to import *

# Exécute une commande système et retourne le résultat.
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("[SUCCESS]")
            print(result.stdout)
        else:
            print("[ERROR]")
            print(result.stdout)
        return result.stdout
    except Exception as e:
        print(f"[EXCEPTION]: {e}")
        return str(e)
    

# Choix de l'attaque
def choix_attaque():
    while True:
        print("Choisissez le type d'attaque à lancer :")
        print("1. Attaque WEP")
        print("2. Attaque WPA")
        print("3. Attaque WPS\n")

        choix = input("Entrez le numéro de l'attaque (1/2/3): ")

        if choix == "1":
            print("[SUCCESS]: Vous avez choisi l'attaque WEP.\n")
            break
        elif choix == "2":
            print("[SUCCESS]: Vous avez choisi l'attaque WPA.\n")
            break
        elif choix == "3":
            print("[SUCCESS]: Vous avez choisi l'attaque WPS.\n")
            break
        else:
            print("[ERROR] : Choix invalide. Veuillez sélectionner 1, 2 ou 3.\n")


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
        print("Quel Interface souhaites tu utiliser :")
        for i, interface in enumerate(interfaces, start=1):
            print(f"{i}. {interface}")

        # Choix de l'Interface
        while True:
            try:
                choice = int(input("\nChoisissez une interface par son numéro : "))
                if 1 <= choice <= len(interfaces):
                    selected_interface = interfaces[choice - 1]
                    print(f"\n[SUCCESS]: Interface sélectionnée : {selected_interface} \n")
                    return selected_interface
                else:
                    print("Veuillez entrer un numéro valide.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")

    except FileNotFoundError:
        print("La commande 'ip' n'est pas disponible sur ce système.")
    except Exception as e:
        print(f"Erreur : {e}")


# Kill les process en cours
def kill_process():
    
    try:
        # Exécution de la commande airmon-ng check kill
        subprocess.run(["sudo", "airmon-ng", "check", "kill"], check=True)
        print("[SUCCESS]: Les processus ont été tués avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR]: Erreur lors de l'exécution de la commande : {e}")


# Lance le mode monitor sur une interface
def start_mode_monitor(interface):
    
    try:
        result = subprocess.run(f"sudo airmon-ng start {interface}", shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"[SUCCESS]: Mode monitor activé sur {interface}")
            return result.stdout.strip()
        else:
            print(f"[ERROR]: Impossible d'activer le mode monitor sur {interface}\n{result.stderr}")
            return None
    except Exception as e:
        print(f"[EXCEPTION]: Une erreur s'est produite : {e}")
        return None
    

# Stop le mode monitor sur une interface
def stop_mode_monitor(interface):
    try:
        result = subprocess.run(f"sudo airmon-ng stop {interface}", shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"[SUCCESS]: Mode moniteur arrêté sur {interface}")
            return result.stdout.strip()
        else:
            print(f"[ERROR]: Impossible d'arrêter le mode moniteur sur {interface}\n{result.stderr}")
            return None
    except Exception as e:
        print(f"[EXCEPTION]: Une erreur s'est produite : {e}")
        return None
 

# Liste les Réseaux Disponible avec leur BSSID et leur channel
def lister_reseaux(interface, fichier_base="Capture/resultats", duree=20, dossier_json="Json"):
    try:
        create_directories()
        capture_wifi_networks(interface, fichier_base, duree)
        reseaux = read_csv_and_extract_networks(fichier_base)        
        save_to_json(reseaux, dossier_json="Result", filename="resultats.json")
        target = display_networks_and_select_target(reseaux, dossier_json)
        save_to_json(target, dossier_json="Target", filename="target.json")
        clean_capture_directory()
        clean_result_directory()
        
    except Exception as e:
        print(f"[ERREUR] Une erreur s'est produite : {e}")



# Capture les paquets de la Target
def capture_from_target_json(interface, attack_type, target_path="Target/target.json", output_dir="Capture"):
    """
    Effectue une capture de paquets à partir des informations du fichier target.json.
    
    :param interface: Interface réseau à utiliser pour la capture (par exemple, "wlan0mon").
    :param target_path: Chemin vers le fichier target.json contenant les informations réseau.
    :param output_dir: Dossier pour enregistrer les fichiers de capture (par défaut "Capture").
    """
    
    try:
        # Lecture des données du fichier JSON
        with open(target_path, "r") as file:
            target_data = json.load(file)
            if not target_data:
                print("Erreur : Le fichier target.json est vide ou mal formaté.")
                return

            # Extraction des informations du réseau
            bssid = target_data["BSSID"]
            channel = target_data["Channel"]

            # Commande pour airodump-ng
            capture_file = os.path.join(output_dir, "capture")
            # command = ["sudo", "airodump-ng", "--bssid", bssid, "--channel", channel, "--write", capture_file, interface]
            
            # Lancement du processus avec Popen pour permettre l'arrêt
            process = subprocess.Popen(
                ["sudo", "airodump-ng", "--bssid", bssid, "--channel", channel, "--write", capture_file, interface],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            if attack_type == "WPA":
                # Capturer les IV et Deduire la clé
                
                time.sleep(30)
                
                # Appel la fonction pour récupérer le nombre d'IV
                get_iv_count("Capture/capture-01.csv")
                
                # Arrêt du processus après la capture
                process.terminate()
                print("Processus de capture terminé.")
                
        
            elif attack_type == "WEP":
                # Capturer les IV et Deduire la clé
                time.sleep(30)
                
                # Arrêt du processus après la capture
                process.terminate()
                print("Processus de capture terminé.")
                
                # Appel la fonction pour récupérer le nombre d'IV
                get_iv_count("Capture/capture-01.csv")

        
            elif attack_type == "WPS":
                print("Lancement de l'attaque WPS... (En cours)")
        
            else:
                print("Bug... Contact KEKE, il y'a un soucis")
            
            


    except FileNotFoundError:
        print(f"Erreur : Le fichier {target_path} n'existe pas.")
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {target_path} n'est pas un JSON valide.")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {str(e)}")
        
        
        
        
#DANS CETTE DEF, JE VEUX lire le  noombre d'iv récolté
def get_iv_count(csv_file):
    """
    Extrait le nombre d'IV (vecteurs d'initialisation) à partir d'un fichier CSV de capture.
    
    :param csv_file: Chemin vers le fichier CSV généré par airodump-ng.
    :return: Le nombre d'IV sous forme d'entier ou None si les données ne sont pas trouvées.
    """
    try:
        with open(csv_file, "r") as file:
            lines = file.readlines()
            data_section = False
            for line in lines:
                if data_section:
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) > 10 and parts[10].isdigit():
                        iv_count = int(parts[10])
                        print(f"Nombre d'IV : {iv_count}")
                        return iv_count
                if line.startswith("BSSID"):
                    data_section = True
    except FileNotFoundError:
        print(f"Erreur : Le fichier {csv_file} n'existe pas.")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {str(e)}")
    return None




# Choix de l'attaque en fonction du fichier Target
def choose_attack_type(target_path="Target/target.json"):
    """
    Choisit le type d'attaque en fonction de la sécurité définie dans target.json.
    
    :param target_path: Chemin vers le fichier target.json contenant les informations réseau.
    :return: Une chaîne indiquant le type d'attaque (WPA, WEP, WPS)
    """
    try:
        with open(target_path, "r") as file:
            target_data = json.load(file)
            if not target_data:
                print("Erreur : Le fichier target.json est vide ou mal formaté.")
                return None
            
            security = target_data.get("Security", "").upper()
            if any(keyword in security for keyword in ["WPA2", "WPA"]):
                attack_type = "WPA"
            elif "WEP" in security:
                attack_type = "WEP"
            elif "WPS" in security:
                attack_type = "WPS"
            else:
                attack_type = None
            
            if attack_type:
                print(f"[SUCCESS] : Type d'attaque sélectionné : {attack_type}")
            else:
                print("[SUCCESS] : Aucun type d'attaque correspondant trouvé.")
            
            if attack_type == "WPA":
                print("Lancement de l'attaque WPA... (En cours)")
        
            elif attack_type == "WEP":
                print("Lancement de l'attaque WEP... (En cours)")
        
            elif attack_type == "WPS":
                print("Lancement de l'attaque WPS... (En cours)")
        
            else:
                print("Bug... Contact KEKE, il y'a un soucis")
            
            return attack_type

    except FileNotFoundError:
        print(f"Erreur : Le fichier {target_path} n'existe pas.")
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier {target_path} n'est pas un JSON valide.")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {str(e)}")
    return None



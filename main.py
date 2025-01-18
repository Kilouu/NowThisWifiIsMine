import pyfiglet
from termcolor import colored
from src.launch_rogue_ap import *
from src.launch_wifi_attack import *
from prerequies import *
import os

if __name__ == "__main__":
    
    ascii_banner = pyfiglet.figlet_format("Now This Wifi Is Mine")
    colored_banner = colored(ascii_banner, 'cyan', attrs=['bold'])
    print(colored_banner)
    
    # Choix du type d'attaque
    while True:
        print("Choisissez le type d'attaque que vous souhaitez effectuer :")
        print("1. Attaque Wifi (WEP/WPA/WPS)")
        print("2. Rogue AP (Evil Twin Attack)\n")
        attack_choice = input("Entrez le numéro de votre choix : ")

        if attack_choice == "1":
            print("Vous avez choisi l'attaque Wifi Classique.")
            launch_wifi_attack()
            break
        
        elif attack_choice == "2":
            print("Vous avez choisi Rogue AP.")
            launch_rogue_ap()
            break
        
        else:
            print("Choix invalide. Veuillez choisir une option valide.")


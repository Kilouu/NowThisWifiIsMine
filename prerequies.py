import os

# Installe les prérequis
def prerequies():
    commands = [
        "sudo apt-get update",
        "sudo apt-get install -y aircrack-ng",
        "sudo apt-get install -y hostapd",
        "sudo apt-get install -y dnsmasq",
        "sudo apt-get install -y iptables",
        "pip install -r requirements.txt"
    ]

    for command in commands:
        os.system(command)


# Exécute la fonction si le fichier est exécuté directement
if __name__ == "__main__":
    prerequies()
import os

# Installe les prérequis
def prerequies():
    commands = [
        "sudo apt-get update",
        "sudo apt-get install -y aircrack-ng",
        "sudo apt-get install -y hostapd",
        "sudo apt-get install -y dnsmasq",
        "sudo apt-get install -y dnsmasq-base",
        "sudo apt-get install -y iptables",
        "sudo apt-get install -y apache2",
        "sudo apt install -y php8.2 libapache2-mod-php8.2",
        "sudo apt install -y php8.2-mysql php8.2-xml php8.2-mbstring php8.2-curl php8.2-zip php8.2-gd php8.2-bcmath",
        "sudo a2enmod php8.2",
        "pip install -r requirements.txt"
    ]

    for command in commands:
        os.system(command)


# Exécute la fonction si le fichier est exécuté directement
if __name__ == "__main__":
    prerequies()
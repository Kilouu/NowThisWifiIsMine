import json
import os

# Sauvegarde dans un fichier JSON
def save_to_json(data, dossier_json, filename):    
    # Sauvegarde les données dans le fichier JSON
    json_file = os.path.join(dossier_json, filename)
    with open(json_file, "w", encoding="utf-8") as json_out:
        json.dump(data, json_out, indent=4, ensure_ascii=False)
    
    print(f"[SUCCESS] : Données sauvegardées dans {json_file}")
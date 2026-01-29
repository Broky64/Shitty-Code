import os
import sqlite3
import pickle
import base64
from flask import Flask, request

app = Flask(__name__)

# 1. CLÉ SECRÈTE HARDCODÉE (Vraiment pas bien)
AWS_SECRET_KEY = "AKIAIMNO78987EXAMPLE"
DATABASE_PASSWORD = "super_secret_password_123!"

@app.route("/vulnerable-action")
def vulnerable():
    user_data = request.args.get("data")
    
    # 2. INJECTION DE COMMANDE (Le Graal des hackers)
    # Si je tape : ?data=; rm -rf /, ton serveur est mort.
    os.system("echo " + user_data)

    # 3. SQL INJECTION (Manipulation de la DB)
    # L'utilisation de f-strings dans une requête SQL est une faille critique.
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = '{user_data}'")
    
    # 4. DÉSÉRIALISATION INSECURE (Exécution de code arbitraire)
    # Charger des données pickle venant de l'utilisateur est suicidaire.
    raw_pickle = base64.b64decode(user_data)
    decoded_data = pickle.loads(raw_pickle)

    return "Scan me if you can!"

if __name__ == "__main__":
    app.run(debug=True) # 5. DEBUG MODE ACTIVÉ EN PROD
# 🔍 Détail des Vulnérabilités & Solutions

## 1. Clés Secrètes Hardcodées

### ❌ Code Vulnérable
```python
AWS_SECRET_KEY = "AKIAIMNO78987EXAMPLE"
DATABASE_PASSWORD = "super_secret_password_123!"
```

### ✅ Solution
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Charge depuis .env

AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
```

### Fichier `.env` (à ignorer avec .gitignore)
```
AWS_SECRET_KEY=votre_vrai_secret
DATABASE_PASSWORD=votre_vraie_password
```

**Outils :** pre-commit hooks, Gitleaks, Truffleog

---

## 2. Injection de Commandes OS

### ❌ Code Vulnérable
```python
import os
user_data = request.args.get("data")
os.system("echo " + user_data)  # DANGER !
```

**Payloads d'exploitation :**
- `; rm -rf /` → Supprime les fichiers
- `| cat /etc/passwd` → Lit les fichiers système
- `&& whoami` → Exécute des commandes

### ✅ Solution
```python
import subprocess

user_data = request.args.get("data", "")

# Utiliser subprocess avec shell=False
result = subprocess.run(
    ["echo", user_data],  # Commande ET arguments séparés
    shell=False,           # Pas d'interprétation shell
    capture_output=True,
    text=True
)
return result.stdout
```

**Pourquoi c'est mieux :**
- Pas d'interprétation des caractères spéciaux
- Les arguments sont traités comme des données, pas du code

---

## 3. SQL Injection

### ❌ Code Vulnérable
```python
import sqlite3
user_id = request.args.get("id")

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# DANGER : f-strings + requête SQL = injection !
cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
```

**Payloads d'exploitation :**
- `' OR '1'='1` → Authentification bypass
- `' UNION SELECT password FROM admin--` → Exfiltration de données
- `'; DROP TABLE users;--` → Suppression de données

### ✅ Solution
```python
import sqlite3

user_id = request.args.get("id")

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Utiliser des placeholders (?) - requête paramétrée
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# Récupérer les résultats
result = cursor.fetchone()
```

**Paramétrage dans différentes DB :**
```python
# SQLite
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# MySQL / Psycopg
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# SQLAlchemy (Recommandé)
from sqlalchemy import text
session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
```

---

## 4. Désérialisation Insecure (Pickle)

### ❌ Code Vulnérable
```python
import pickle
import base64

user_data = request.args.get("data")

# DANGER : pickle.loads() peut exécuter du code arbitraire !
raw_pickle = base64.b64decode(user_data)
decoded_data = pickle.loads(raw_pickle)
```

**Pourquoi c'est dangereux :**
Pickle exécute du code lors de la désérialisation. Un attaquant peut créer un payload malveillant.

**Générer un payload d'exploitation :**
```python
import pickle
import base64
import os

# Créer un payload qui exécute `whoami`
class RCE:
    def __reduce__(self):
        return (os.system, ('whoami',))

payload = pickle.dumps(RCE())
encoded = base64.b64encode(payload).decode()
print(encoded)
# Envoyer à : ?data={encoded}
```

### ✅ Solution
```python
import json
import base64

user_data = request.args.get("data")

try:
    # JSON est sûr car il ne peut pas exécuter du code
    decoded_data = json.loads(user_data)
except json.JSONDecodeError:
    return "Invalid JSON", 400
```

**Comparaison :**
| Format | Sûr ? | Utilisation |
|--------|-------|-----------|
| `json` | ✅ Oui | Données structurées |
| `pickle` | ❌ Non | Ne jamais utiliser pour l'input utilisateur |
| `msgpack` | ⚠️ Conditionnel | Avec validation stricte |

---

## 5. Mode Debug Activé en Production

### ❌ Code Vulnérable
```python
if __name__ == "__main__":
    app.run(debug=True)  # Mode debug = Mode risqué !
```

**Risques du debug mode :**
- Stack traces détaillées = révélation de code
- Accès au débogueur interactif (Werkzeug debugger)
- Rechargement automatique des modules
- Exposition de variables d'environnement

### ✅ Solution
```python
import os

if __name__ == "__main__":
    # Debug mode = False en production
    debug_mode = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug_mode)
```

Ou avec configuration Flask :
```python
from flask import Flask

app = Flask(__name__)
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", False)
```

**Fichier `.env` pour dev :**
```
FLASK_DEBUG=True
```

**En production :**
```
FLASK_DEBUG=False
```

---

## 🛡️ Bonnes Pratiques Générales

### 1. **Validation des Entrées**
```python
from urllib.parse import quote_plus
from flask import escape

user_input = request.args.get("data", "")

# Valider et nettoyer
if not user_input.isalnum():
    return "Invalid input", 400

# Ou échapper pour l'HTML
safe_output = escape(user_input)
```

### 2. **Utiliser un WAF (Web Application Firewall)**
- ModSecurity
- CloudFlare
- AWS WAF

### 3. **Logging & Monitoring**
```python
import logging

logging.warning(f"Suspicious input detected: {user_input}")
```

### 4. **Headers de Sécurité**
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

### 5. **Authentification & Autorisation**
```python
from flask_login import login_required, current_user

@app.route("/data")
@login_required
def get_data():
    if not current_user.is_admin:
        return "Forbidden", 403
    return "Admin data"
```

---

## 🔗 Outils de Détection

| Outil | Utilité |
|-------|---------|
| **Bandit** | Scan les failles Python |
| **Semgrep** | SAST multi-langage |
| **SonarQube** | Analyse statique complète |
| **OWASP ZAP** | Test de sécurité web dynamique |
| **Snyk** | Scan des dépendances vulnérables |
| **Gitleaks** | Détecte les secrets dans Git |

---

**Dernière mise à jour :** January 2026

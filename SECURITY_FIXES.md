# 🔍 Vulnerabilities Detail & Solutions

## 1. Hardcoded Secret Keys

### ❌ Vulnerable Code
```python
AWS_SECRET_KEY = "AKIAIMNO78987EXAMPLE"
DATABASE_PASSWORD = "super_secret_password_123!"
```

### ✅ Solution
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
```

### .env File (must be ignored with .gitignore)
```
AWS_SECRET_KEY=your_real_secret
DATABASE_PASSWORD=your_real_password
```

**Tools :** pre-commit hooks, Gitleaks, Truffleog

---

## 2. OS Command Injection

### ❌ Vulnerable Code
```python
import os
user_data = request.args.get("data")
os.system("echo " + user_data)  # DANGER!
```

**Exploitation Payloads :**
- `; rm -rf /` → Deletes files
- `| cat /etc/passwd` → Reads system files
- `&& whoami` → Executes commands

### ✅ Solution
```python
import subprocess

user_data = request.args.get("data", "")

# Use subprocess with shell=False
result = subprocess.run(
    ["echo", user_data],  # Command AND arguments separated
    shell=False,           # No shell interpretation
    capture_output=True,
    text=True
)
return result.stdout
```

**Why it's better:**
- Special characters are not interpreted
- Arguments are treated as data, not code

---

## 3. SQL Injection

### ❌ Vulnerable Code
```python
import sqlite3
user_id = request.args.get("id")

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# DANGER: f-strings + SQL query = injection!
cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
```

**Exploitation Payloads :**
- `' OR '1'='1` → Authentication bypass
- `' UNION SELECT password FROM admin--` → Data exfiltration
- `'; DROP TABLE users;--` → Data deletion

### ✅ Solution
```python
import sqlite3

user_id = request.args.get("id")

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Use placeholders (?) - parameterized query
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# Fetch results
result = cursor.fetchone()
```

**Parameterization in different databases :**
```python
# SQLite
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# MySQL / Psycopg
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# SQLAlchemy (Recommended)
from sqlalchemy import text
session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
```

---

## 4. Insecure Deserialization (Pickle)

### ❌ Vulnerable Code
```python
import pickle
import base64

user_data = request.args.get("data")

# DANGER: pickle.loads() can execute arbitrary code!
raw_pickle = base64.b64decode(user_data)
decoded_data = pickle.loads(raw_pickle)
```

**Why it's dangerous:**
Pickle executes code during deserialization. An attacker can create a malicious payload.

**Generate an exploitation payload:**
```python
import pickle
import base64
import os

# Create a payload that executes `whoami`
class RCE:
    def __reduce__(self):
        return (os.system, ('whoami',))

payload = pickle.dumps(RCE())
encoded = base64.b64encode(payload).decode()
print(encoded)
# Send to: ?data={encoded}
```

### ✅ Solution
```python
import json
import base64

user_data = request.args.get("data")

try:
    # JSON is safe because it cannot execute code
    decoded_data = json.loads(user_data)
except json.JSONDecodeError:
    return "Invalid JSON", 400
```

**Comparison :**
| Format | Safe? | Usage |
|--------|-------|-----------|
| `json` | ✅ Yes | Structured data |
| `pickle` | ❌ No | Never use for user input |
| `msgpack` | ⚠️ Conditional | With strict validation |

---

## 5. Debug Mode Enabled in Production

### ❌ Vulnerable Code
```python
if __name__ == "__main__":
    app.run(debug=True)  # Debug mode = High risk!
```

**Risks of debug mode :**
- Detailed stack traces = Code exposure
- Access to interactive debugger (Werkzeug debugger)
- Automatic module reloading
- Exposure of environment variables

### ✅ Solution
```python
import os

if __name__ == "__main__":
    # Debug mode = False in production
    debug_mode = os.getenv("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug_mode)
```

Or with Flask configuration :
```python
from flask import Flask

app = Flask(__name__)
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", False)
```

**.env file for dev :**
```
FLASK_DEBUG=True
```

**In production :**
```
FLASK_DEBUG=False
```

---

## 🛡️ General Security Best Practices

### 1. **Input Validation**
```python
from urllib.parse import quote_plus
from flask import escape

user_input = request.args.get("data", "")

# Validate and clean
if not user_input.isalnum():
    return "Invalid input", 400

# Or escape for HTML
safe_output = escape(user_input)
```

### 2. **Use a WAF (Web Application Firewall)**
- ModSecurity
- CloudFlare
- AWS WAF

### 3. **Logging & Monitoring**
```python
import logging

logging.warning(f"Suspicious input detected: {user_input}")
```

### 4. **Security Headers**
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

### 5. **Authentication & Authorization**
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

## 🔗 Detection Tools

| Tool | Purpose |
|-------|---------|
| **Bandit** | Scan Python security flaws |
| **Semgrep** | Multi-language SAST |
| **SonarQube** | Complete static analysis |
| **OWASP ZAP** | Dynamic web security testing |
| **Snyk** | Scan vulnerable dependencies |
| **Gitleaks** | Detect secrets in Git |

---

**Last updated :** January 2026

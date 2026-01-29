# 🚨 Security Vulnerabilities Repository (Demo)

## 📋 Repository Objective

This repository is an **intentional collection of security flaws**, bad practices, and common vulnerabilities in web applications. 

**⚠️ WARNING :** This code is intentionally **VULNERABLE** and designed for **educational purposes only** to:
- Learn how to identify security vulnerabilities
- Understand how hackers exploit these flaws
- Train developers in security best practices
- Test security scanning tools (SAST, DAST, etc.)

**❌ DO NOT USE THIS CODE IN PRODUCTION!**

---

## 🔴 Documented Vulnerabilities

### 1. **Hardcoded Secret Keys** (CWE-798)
```python
AWS_SECRET_KEY = "AKIAIMNO78987EXAMPLE"
DATABASE_PASSWORD = "super_secret_password_123!"
```
**Risk :** Attackers can access external services.
**Best Practice :** Use environment variables or a secrets manager.

---

### 2. **OS Command Injection** (CWE-78)
```python
os.system("echo " + user_data)
```
**Risk :** An attacker can execute arbitrary commands.
**Exploitation Payload :**
```
?data=; rm -rf /
?data=; cat /etc/passwd
```
**Best Practice :** Use `subprocess` with `shell=False` or avoid shell commands.

---

### 3. **SQL Injection** (CWE-89)
```python
cursor.execute(f"SELECT * FROM users WHERE id = '{user_data}'")
```
**Risk :** Database manipulation or data exfiltration.
**Exploitation Payload :**
```
?data=' OR '1'='1
?data=' UNION SELECT * FROM admin--
```
**Best Practice :** Use parameterized queries (prepared statements).

---

### 4. **Insecure Deserialization** (CWE-502)
```python
raw_pickle = base64.b64decode(user_data)
decoded_data = pickle.loads(raw_pickle)
```
**Risk :** Arbitrary code execution via pickle.
**Best Practice :** Use `json` instead of `pickle` or strictly validate data.

---

### 5. **Debug Mode Enabled in Production** (CWE-215)
```python
app.run(debug=True)
```
**Risk :** Exposure of stack traces, sensitive information, and access to interactive debugger.
**Best Practice :** Disable debug in production (`debug=False`).

---

## 📁 Repository Structure

```
.
├── README.md                      # This file
├── SECURITY_FIXES.md              # Solutions and best practices
├── CODE_OF_CONDUCT.md             # Responsible use policy
├── QUICKSTART.md                  # Installation & quick start guide
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Setup for local testing
├── .env.example                   # Environment variables template
├── .gitignore                     # Files to ignore
├── python/
│   ├── main.py                    # Intentionally vulnerable code
│   └── requirements.txt           # Python dependencies
└── tests/                         # Exploitation tests (future)
    └── test_vulnerabilities.py   
```

---

## 🎯 Use Cases

### ✅ Appropriate Uses

1. **Cybersecurity Training**
   - Understand OWASP Top 10 vulnerabilities
   - Learn exploitation and mitigations

2. **Security Testing (Pentesting)**
   - Verify security scanning tools (SAST/DAST)
   - Validate detection rules

3. **Security Development**
   - Benchmark security linting rules
   - Test security frameworks

### ❌ Inappropriate Uses

- Deploy this code in production
- Use for attacking other systems
- Ignore security warnings

---

## 🚀 Installation & Usage

### Prerequisites
- Python 3.8+
- pip or poetry

### Installation
```bash
git clone https://github.com/username/security-vulnerabilities.git
cd security-vulnerabilities

pip install -r python/requirements.txt
```

### Run the Application (Local Only)
```bash
python python/main.py
```

The app starts on `http://localhost:5000`

---

## 🧪 Testing Vulnerabilities

### Example: SQL Injection
```bash
curl "http://localhost:5000/vulnerable-action?data=' OR '1'='1"
```

### Example: Command Injection
```bash
curl "http://localhost:5000/vulnerable-action?data=;whoami"
```

---

## 📚 Learning Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)

---

## ⚖️ License

This project is under the **MIT License**. However, **use it responsibly**.

---

## ⚠️ Disclaimer

**The authors of this repository are not responsible for damages caused by malicious or irresponsible use of this code.**

This tool is reserved for education and authorized security testing in a controlled environment.

---

## 📝 Contributing

Contributions to add new documented vulnerabilities are welcome! 🎓

---

**Last updated :** January 2026

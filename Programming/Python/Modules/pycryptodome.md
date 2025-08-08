
# PyCryptodome – Complete Pentester & Red Team Guide

---

## 1. Overview

**PyCryptodome** is a self-contained Python cryptography library for encryption, decryption, hashing, and digital signatures.  
For pentesters/red teamers, it’s invaluable for:
- Encrypting C2 communications
- Encoding payloads to evade detection
- Decrypting captured data during engagements
- Implementing cryptographic attacks

---

## 2. Installation

```bash
pip install pycryptodome
```

Import styles:
```python
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
```

---

## 3. Symmetric Encryption (AES)

### AES Encryption Example
```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)  # AES-128
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce

ciphertext, tag = cipher.encrypt_and_digest(b"Secret Message")

print(ciphertext, tag, nonce)
```

### AES Decryption Example
```python
from Crypto.Cipher import AES

cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)

try:
    cipher.verify(tag)
    print("Message is authentic:", plaintext)
except ValueError:
    print("Key incorrect or message corrupted")
```

---

## 4. Asymmetric Encryption (RSA)

### Generate RSA Key Pair
```python
from Crypto.PublicKey import RSA

key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()
```

### Encrypt/Decrypt with RSA
```python
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

public_key = RSA.import_key(open("public.pem").read())
private_key = RSA.import_key(open("private.pem").read())

cipher_rsa = PKCS1_OAEP.new(public_key)
ciphertext = cipher_rsa.encrypt(b"Secret Data")

cipher_rsa = PKCS1_OAEP.new(private_key)
plaintext = cipher_rsa.decrypt(ciphertext)
```

---

## 5. Hashing & Integrity

```python
from Crypto.Hash import SHA256

h = SHA256.new()
h.update(b"password123")
print(h.hexdigest())
```

---

## 6. Digital Signatures

```python
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

message = b"Test Message"
key = RSA.generate(2048)
h = SHA256.new(message)

signature = pkcs1_15.new(key).sign(h)

try:
    pkcs1_15.new(key.publickey()).verify(h, signature)
    print("Signature valid")
except (ValueError, TypeError):
    print("Signature invalid")
```

---

## 7. Common Pentest Use Cases

- Encrypting reverse shell traffic to eva


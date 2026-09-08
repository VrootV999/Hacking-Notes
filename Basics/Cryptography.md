## What we'll be learning  

- Basics of Crptography
- Understand encryption algorithms and their applications
- Hashing functions and digital signatures
- Cryptanalysis techniques
- Vulnerabilties and exploits and stay updated

  

---

  

## **What is Encryption?**

**Encryption** is the process of converting data (plaintext) into an unreadable form (ciphertext) to protect it from unauthorized access. It ensures confidentiality by allowing only authorized parties with the correct decryption key to convert the ciphertext back into plaintext.

  

### Plaintext: original, readable data which is fed into an encryption algorithm

### Ciphertext: unreadable, encrypted output of plaintext

  


---

  

## **Symmetrical Encryption**

Symmetrical encryption uses the **same key** for both encryption and decryption. Both parties must possess this shared secret key, making key distribution a major concern.

  

```JavaScript
Person A (Sender) ---(Shared Secret Key)---> [ Encryption Algorithm ] --> [ Ciphertext ]
Person B (Receiver) ---(Same Shared Key)---> [ Decryption Algorithm ] --> [ Plaintext ]
```

  

### **Symmetric Encryption Algorithms**

1. **AES (Advanced Encryption Standard)**
    - **Block Size**: 128 bits
    - **Key Sizes**: 128, 192, 256 bits
    - **Security**: Very secure and widely adopted. As of today, AES-256 is resistant to brute-force attacks.
    - **Vulnerabilities**: Side-channel attacks (timing/power analysis) can reveal keys if improperly implemented.
2. **DES (Data Encryption Standard)**
    - **Block Size**: 64 bits
    - **Key Size**: 56 bits
    - **Security**: Insecure due to short key length; vulnerable to brute-force attacks.
    - **How Hackers Crack It**: Brute-force and linear cryptanalysis.
3. **Blowfish**
    - **Block Size**: 64 bits
    - **Key Size**: 32 to 448 bits
    - **Security**: Secure, but vulnerable to birthday attacks due to its small block size.
    - **How Hackers Crack It**: Attacks mainly target bad implementations.
4. **3DES (Triple DES)**
    - **Block Size**: 64 bits
    - **Key Size**: 168 bits (effectively ~112 bits)
    - **Security**: More secure than DES, but slow and vulnerable to meet-in-the-middle attacks.
    - **How Hackers Crack It**: Brute-force is still possible, and it's being replaced by AES.
5. **2DES (Double DES)**
    - **Block Size**: 64 bits
    - **Key Size**: 112 bits
    - **Security**: More secure than DES but vulnerable to meet-in-the-middle attacks.
    - **How Hackers Crack It**: Meet-in-the-middle can reduce the complexity of attacks.
6. **IDEA (International Data Encryption Algorithm)**
    - **Block Size**: 64 bits
    - **Key Size**: 128 bits
    - **Security**: Secure, but not as commonly used today.
    - **How Hackers Crack It**: No major vulnerabilities, but patent restrictions limit use.
7. **RC4 (Rivest Cipher 4)**
    - **Stream Cipher**
    - **Key Size**: 40 to 2048 bits
    - **Security**: Known vulnerabilities in its output; insecure for use in most modern systems (e.g., TLS).
    - **How Hackers Crack It**: Weaknesses in the keystream allow for key recovery attacks.
8. **RC5**
    - **Block Size**: Variable (32, 64, or 128 bits)
    - **Key Size**: Variable (up to 2040 bits)
    - **Security**: Stronger than RC4, but not as widely used.
    - **How Hackers Crack It**: No known practical attacks, but it’s resource-intensive.
9. **SkipJack**
    - **Block Size**: 64 bits
    - **Key Size**: 80 bits
    - **Security**: Developed by the NSA, but its security was controversial.
    - **How Hackers Crack It**: Largely deprecated due to the small key size.
10. **Quad**
    - **Block Size**: 128 bits
    - **Key Size**: Variable
    - **Security**: Designed for high performance; not widely used.
    - **How Hackers Crack It**: Largely theoretical; no widespread implementation.
11. **RC6**
    
    - **Block Size**: 128 bits
    - **Key Size**: Up to 2048 bits
    - **Security**: A finalist in the AES competition but not widely adopted.
    - **How Hackers Crack It**: No practical attacks known; it's considered secure.
    
      
    
      
    

---

  

## **Asymmetrical Encryption**

Asymmetrical encryption uses **two keys**: a public key for encryption and a private key for decryption. Only the private key, held by the receiver, can decrypt the data.

  

```JavaScript
Person A (Sender) ---(Person B’s Public Key)---> [ Encryption Algorithm ] --> [ Ciphertext ]
Person B (Receiver) ---(Person B’s Private Key)---> [ Decryption Algorithm ] --> [ Plaintext ]
```

### **Asymmetric Encryption Algorithms**

1. **RSA (Rivest-Shamir-Adleman)**
    - **Key Size**: 1024, 2048, 4096+ bits
    - **Security**: Secure with large key sizes, but vulnerable to factoring attacks for smaller keys.
    - **How Hackers Crack It**: Prime factorization attacks (e.g., using quantum computing or lattice methods).
2. **ECC (Elliptic Curve Cryptography)**
    - **Key Size**: 160 to 521 bits
    - **Security**: Offers high security with shorter keys compared to RSA.
    - **How Hackers Crack It**: Side-channel attacks and improperly chosen curves.
3. **ElGamal**
    - **Key Size**: 1024, 2048+ bits
    - **Security**: Based on the discrete logarithm problem; secure with large keys.
    - **How Hackers Crack It**: Brute-force attacks can be attempted, but large keys are secure.
4. **Diffie-Hellman (DH)**
    - **Key Size**: Variable (usually 2048+ bits)
    - **Security**: Used for secure key exchange. Vulnerable to man-in-the-middle if not authenticated.
    - **How Hackers Crack It**: Lack of authentication can allow MITM attacks.

---

## **Hashing**

**Hashing** is the process of converting data into a fixed-length string of characters, which is typically a digest that represents the original data. Hashes are designed to be irreversible.

### **Hashing Algorithms**

1. **MD2**
    - **Hash Length**: 128 bits
    - **Security**: Insecure; vulnerable to collision attacks.
    - **How Hackers Crack It**: Collision attacks are feasible.
2. **MD4**
    - **Hash Length**: 128 bits
    - **Security**: Broken; vulnerable to collision and preimage attacks.
    - **How Hackers Crack It**: Collision attacks have been demonstrated.
3. **MD5**
    - **Hash Length**: 128 bits
    - **Security**: Insecure due to collision vulnerabilities.
    - **How Hackers Crack It**: Rainbow tables, precomputed attacks, and collisions.
4. **HAVAL**
    - **Hash Length**: 128, 160, 192, 224, 256 bits
    - **Security**: No known vulnerabilities for larger sizes, but not widely used.
    - **How Hackers Crack It**: Brute-force attacks are possible with shorter hash lengths.
5. **SHA-0**
    - **Hash Length**: 160 bits
    - **Security**: Broken due to vulnerabilities found by researchers.
    - **How Hackers Crack It**: Collision attacks.
6. **SHA-1**
    - **Hash Length**: 160 bits
    - **Security**: Broken; collision attacks are feasible.
    - **How Hackers Crack It**: Researchers have shown how to generate collisions.
7. **SHA-2**
    - **Hash Lengths**: 224, 256, 384, 512 bits
    - **Subfamilies**: SHA-224, SHA-256, SHA-384, SHA-512
    - **Security**: Secure; widely used in modern systems (e.g., SSL certificates).
    - **How Hackers Crack It**: No feasible attacks on SHA-2, but weak salts can weaken the security.
8. **SHA-3**
    - **Hash Lengths**: Variable (SHA3-224, SHA3-256, SHA3-384, SHA3-512)
    - **Security**: Secure and based on the Keccak algorithm; no known vulnerabilities.
    - **How Hackers Crack It**: No practical attacks known.
9. **Whirlpool**
    - **Hash Length**: 512 bits
    - **Security**: No known vulnerabilities.
    - **How Hackers Crack It**: Strong against brute-force; no major weaknesses.
10. **RIPEMD**
	- **Hash Length**: 128, 160, 256, 320 bits
	- **Security**: RIPEMD-128 is insecure; RIPEMD-160 is still secure.
	- **How Hackers Crack It**: Collision attacks possible with the smaller variants.


---

## **Certificates and Signatures**

### **Digital Certificates**

A **digital certificate** is an electronic document used to prove ownership of a public key. It binds the key to the identity of the owner (individual, organization, server).

- **Components**: Public key, owner’s identity, Certificate Authority (CA) signature.
- **Use**: Ensures that public keys belong to the right entity, preventing man-in-the-middle attacks.

### **Digital Signature**

A **digital signature** is a cryptographic way to verify the authenticity and integrity of a message or document. It is created using the sender’s private key and can be verified using the sender’s public key.

  

> [!important]  
> NOTE:
>  Digital certificate: Contains Digital signature, public key, other identification information Digital Signature: Hash of the message.  

  

---

## Complete Flow of Data

  

### Using Symetric Key Flow

```JavaScript
[Person A (Sender)] ---(Shared Secret Key)-------------------> [ Encryption ] 
          |                                                          |
   [Digital Certificate]                                       [ Ciphertext ] 
          |                                                          |
          |------------------------------------------------> [Person B (Receiver)] 
                                                                     |
                                                        [Digital Certificate Validation]
                                                                     |
                                                         [Shared Secret Key Validation]
                                                                     |
                                                                [ Plaintext ]
```

  

### Using Asymetric Key Flow

  

```JavaScript
[Person A (Sender)] ---(Person B's Public Key)----- ---------> [ Encryption ]
          |                             |                           |
          |               (validation)--+                           |
          |                             |                           |
[Digital Certificate (Person B)]--------|                      [ Ciphertext ]
          |                                                         |
          |---------------------------------------------> [Person B (Receiver)] 
                                                                    |
                                                     [Digital Certificate Validation]
                                                                    |
                                                    [Person B's Private Key to decrypt]
                                                                    |
                                                               [ Plaintext ]
```

---

  

## **PKI (Public Key Infrastructure)**

**PKI** is the framework that manages the creation, distribution, and revocation of digital certificates. It provides secure key management for encryption, ensuring that public keys are authentic and belong to the correct owners.

### **Components**:

- **Certificate Authority (CA)**: Issues digital certificates.
- **Registration Authority (RA)**: Verifies user identities before the CA issues certificates.
- **Certificate Revocation List (CRL)**: A list of certificates that have been revoked before their expiration date.

  

---

## **Types of Cryptographic Attacks**

1. **Ciphertext-Only Attack (COA)**:
    - The attacker only has access to the ciphertext and tries to deduce the plaintext or key.
    - **Defense**: Use strong encryption algorithms.
2. **Known-Plaintext Attack (KPA)**:
    - The attacker knows some of the plaintext and corresponding ciphertext and tries to deduce the key.
    - **Defense**: Strong encryption and frequent key rotation.
3. **Chosen-Plaintext Attack (CPA)**:
    - The attacker can choose plaintexts and observe the corresponding ciphertext.
    - **Defense**: Strong, randomized encryption schemes.
4. **Chosen-Ciphertext Attack (CCA)**:
    - The attacker can choose ciphertexts and obtain their corresponding plaintexts.
    - **Defense**: Algorithms like RSA-OAEP are designed to resist CCA.
5. **Adaptive Chosen-Ciphertext Attack (CCA2)**:
    - The attacker adapts their queries based on previous ciphertexts to learn more about the plaintext or key.

  

---

## Caesar Cipher:

- It is the way of encrypting message with place shifiting
- Each letter in the Alphabets is a number A=0 and z=25
- P=PlainText
- C=Ciphertext
- k = Key
- Caesar Cipher = Always +3
- C = E(p,k) modulus 26
-  Ex: letter n
		C = (13+3) mod 26
		C = (16) mod 26
		C = 16
	- same for even if the letter is Z

---

## XOR
- or known as exclusive or:
- Uses Boolean to Encrypt with binary
- for example:
	  CAT = 
	  C = 1000011
	  A = 1000001
	  T = 1010100
	1000011        1000001        1010100      === CAT
    1000100       1001111          1000111      === DOG     (Encryption Word)
    0000111        0001110         0010011       (ciphertext)
    That's how you encrypt the message and Decryption is the reverse of the above

---

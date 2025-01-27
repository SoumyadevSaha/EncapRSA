# **EncapRSA: Encapsulation and Decapsulation Framework Using RSA**

### Author: Soumyadev Saha

---

## **Overview**
**EncapRSA** is a secure RSA-based key exchange module that implements encapsulation and decapsulation of random symmetric keys. This library utilizes modular arithmetic and cryptographic hashing to ensure confidentiality and integrity of exchanged keys. The algorithm is robustly designed to hash public/private keys and encapsulated values, guaranteeing secure transmission of symmetric keys.

---

## **Key Features**
- RSA key generation with hashed public and private keys.
- Encapsulation of random symmetric keys using the hashed public key.
- Decapsulation of the same symmetric key using the hashed private key.
- Random seed initialization using a combination of salt and timestamp for randomness.

## **Mathematical Foundations**

### **1. RSA Algorithm**
The RSA algorithm is based on the following steps:

1. **Key Generation**:
   - Select two large prime numbers \( p \) and \( q \).
   - Compute:
     \[
     n = p \cdot q
     \]
     \[
     \phi(n) = (p-1) \cdot (q-1)
     \]
   - Choose \( e \), such that \( 1 < e < \phi(n) \) and:
     \[
     \gcd(e, \phi(n)) = 1
     \]
   - Compute the modular multiplicative inverse of \( e \) modulo \( \phi(n) \):
     \[
     d = e^{-1} \mod \phi(n)
     \]

2. **Public and Private Keys**:
   - Public Key: \( (e, n) \)
   - Private Key: \( (d, n) \)

3. **Encryption and Decryption**:
   - For a message \( M \), where \( 0 \leq M < n \):
     \[
     C = M^e \mod n
     \]
   - Decryption:
     \[
     M = C^d \mod n
     \]

---

### **2. Encapsulation and Decapsulation**

#### **Encapsulation**:
1. A random symmetric key \( K \) is selected:
   \[
   K \in \{1, 2, \dots, n-1\}
   \]
2. The symmetric key is encapsulated using the public key \( (e, n) \):
   \[
   C = K^e \mod n
   \]

#### **Decapsulation**:
1. Using the private key \( (d, n) \), the original symmetric key \( K \) is recovered:
   \[
   K = C^d \mod n
   \]

---

### **3. Why It Works**

The regeneration of the same \( K \) is guaranteed due to **Fermat's Little Theorem** and properties of modular arithmetic:

#### **Fermat's Little Theorem**:
For a prime number \( p \) and any integer \( a \) such that \( a \) is not divisible by \( p \):
\[
a^{p-1} \equiv 1 \pmod{p}
\]

#### **Proof of Correctness**:
1. Since \( d \) is the modular multiplicative inverse of \( e \):
   \[
   e \cdot d \equiv 1 \pmod{\phi(n)}
   \]
   This implies:
   \[
   e \cdot d = k \cdot \phi(n) + 1 \quad \text{for some integer } k.
   \]

2. During decapsulation:
   \[
   K = (K^e)^d \mod n
   \]
   Substituting \( e \cdot d \):
   \[
   K = K^{k \cdot \phi(n) + 1} \mod n
   \]

3. Using modular arithmetic properties:
   \[
   K^{\phi(n)} \equiv 1 \pmod{n}
   \]
   Hence:
   \[
   K^{k \cdot \phi(n)} \cdot K \equiv K \pmod{n}
   \]

Thus, the original \( K \) is recovered.

---

## **Usage**

### **Key Generation**
```python
from EncapRSA import EncapRSA

ek, dk = EncapRSA.generate_keys(digits=10, salt="my_secure_salt")
```

### **Encapsulation**
```python
hashed_c, hashed_K = EncapRSA.encapsulate(ek, salt="my_secure_salt")
```

### **Decapsulation**
```python
hashed_K_decapsulated = EncapRSA.decapsulate(hashed_c, dk, salt="my_secure_salt")
```

---

## **Symmetric Key Exchange**

1. **Encapsulation**:
   - Generate a random symmetric key \( K \).
   - Encrypt \( K \) using the public key \( ek \) to produce the encapsulated value \( C \).

2. **Decapsulation**:
   - Recover \( K \) using the private key \( dk \).
   - Verify that the regenerated \( K \) matches the original.

---

### **Advantages**
- **Confidentiality**: Public and private keys, as well as the encapsulated values, are securely hashed.
- **Correctness**: Fermat's theorem ensures reliable key recovery.
- **Uniqueness**: The use of salt and timestamps ensures that random values are unique.

---

## **Example Output**

```plaintext
Hashed Public Key (ek): b23c9d8c3ab12f1...
Hashed Private Key (dk): a192dc8372b9e7...
Hashed Encapsulated Value (c): f45bc38129ac7d...
Hashed Original Random Value (K): e79fcb8318a2b7...

Decapsulation successful!
```

---

### **Note**
Ensure that the `encap_rsa` module is correctly implemented and imported into your Python environment for seamless execution of the key generation, encapsulation, and decapsulation processes.

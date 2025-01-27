import random
import base64
from sympy import isprime, mod_inverse
from math import gcd
from time import time


class EncapRSA:
    """A secure RSA-based key exchange module with base64 encoded public and private keys."""

    @staticmethod
    def _initialize_seed(salt: str) -> None:
        """Initialize the random seed using a salt and the current timestamp."""
        numeric_salt = sum(ord(char) for char in salt)
        random.seed(numeric_salt + int(time() * 1000))

    @staticmethod
    def _generate_prime(digits: int) -> int:
        """Generate a prime number with the specified digits."""
        while True:
            try:
                candidate = random.randint(10**(digits - 1), 10**digits - 1)
                if isprime(candidate):
                    return candidate
            except Exception as e:
                print(f"Error generating prime: {e}")
                continue

    @staticmethod
    def _encode_pair(value1: int, value2: int) -> str:
        """Encode two integers into a base64 string."""
        try:
            combined = f"{value1}:{value2}".encode("utf-8")
            return base64.b64encode(combined).decode("utf-8")
        except Exception as e:
            print(f"Error encoding pair: {e}")
            raise ValueError("Error encoding the pair.")

    @staticmethod
    def _decode_pair(encoded_str: str) -> tuple:
        """Decode a base64 string back into two integers."""
        try:
            decoded = base64.b64decode(encoded_str.encode("utf-8")).decode("utf-8")
            value1, value2 = decoded.split(":")
            return int(value1), int(value2)
        except Exception as e:
            print(f"Error decoding pair: {e}")
            raise ValueError("Error decoding the pair. Ensure the encoded string is in the correct format.")

    @staticmethod
    def generate_keys(digits: int, salt: str) -> tuple:
        """Generate base64 encoded public (ek) and private (dk) keys."""
        try:
            EncapRSA._initialize_seed(salt)
            p = EncapRSA._generate_prime(digits)
            q = EncapRSA._generate_prime(digits)
            while p == q:
                q = EncapRSA._generate_prime(digits)

            n = p * q
            phi_n = (p - 1) * (q - 1)

            e = random.randint(2, phi_n - 1)
            while gcd(e, phi_n) != 1:
                e = random.randint(2, phi_n - 1)

            d = mod_inverse(e, phi_n)

            ek = EncapRSA._encode_pair(e, n)
            dk = EncapRSA._encode_pair(d, n)

            return ek, dk
        except Exception as e:
            print(f"Error generating keys: {e}")
            raise ValueError("Error during key generation.")

    @staticmethod
    def encapsulate(public_key: str, salt: str) -> tuple:
        """Encapsulate a random value using the public key."""
        try:
            EncapRSA._initialize_seed(salt)
            e, n = EncapRSA._decode_pair(public_key)
            K = random.randint(1, n - 1)
            c = pow(K, e, n)
            encoded_c = base64.b64encode(str(c).encode("utf-8")).decode("utf-8")
            encoded_K = base64.b64encode(str(K).encode("utf-8")).decode("utf-8")
            return encoded_c, encoded_K
        except Exception as e:
            print(f"Error during encapsulation: {e}")
            raise ValueError("Error during encapsulation. Ensure the public key is valid.")

    @staticmethod
    def decapsulate(encapsulated_value: str, private_key: str, salt: str) -> str:
        """Decapsulate the original value using the private key."""
        try:
            c = int(base64.b64decode(encapsulated_value.encode("utf-8")).decode("utf-8"))
            d, n = EncapRSA._decode_pair(private_key)
            K = pow(c, d, n)
            return base64.b64encode(str(K).encode("utf-8")).decode("utf-8")
        except Exception as e:
            print(f"Error during decapsulation: {e}")
            raise ValueError("Error during decapsulation. Ensure the encapsulated value and private key are valid.")


# Example Usage
if __name__ == "__main__":
    try:
        # Generate keys
        rsa = EncapRSA()
        ek, dk = rsa.generate_keys(digits=10, salt="secure_salt")
        print(f"Encoded Public Key (ek): {ek}")
        print(f"Encoded Private Key (dk): {dk}")

        # Encapsulation
        c_encoded, K_encoded_original = rsa.encapsulate(ek, salt="secure_salt")
        print(f"Encoded Encapsulated Value (c): {c_encoded}")
        print(f"Encoded Original Random Value (K): {K_encoded_original}")

        # Decapsulation
        K_encoded_decapsulated = rsa.decapsulate(c_encoded, dk, salt="secure_salt")
        print(f"Encoded Decapsulated Value (K): {K_encoded_decapsulated}")

        # Verify
        assert K_encoded_original == K_encoded_decapsulated, "Decapsulation failed!"
        print("Decapsulation successful!")

    except Exception as e:
        print(f"Error: {e}")

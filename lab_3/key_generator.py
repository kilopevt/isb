import pickle
import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


class KeyGenerator:
    def __init__(self, symmetric_key_length=256):
        """
        Initialize the key generator with specified symmetric key length

        :param symmetric_key_length: Length of symmetric key in bits (128, 192, or 256)
        """
        if symmetric_key_length not in [128, 192, 256]:
            raise ValueError("Key length must be 128, 192 or 256 bit")
        self.symmetric_key_length = symmetric_key_length
        self.backend = default_backend()

    def generate_symmetric_key(self):
        """
        Generates a random symmetric key for Camellia encryption

        :return: Randomly generated symmetric key of specified length
        """
        return os.urandom(self.symmetric_key_length // 8)

    def generate_asymmetric_key(self):
        """
        Generates RSA public/private key pair

        :return: (private_key, public_key) RSA key pair
        """
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=self.backend
            )
            public_key = private_key.public_key()
            return private_key, public_key
        except Exception as e:
            raise Exception(f"Error at generate asymmetric key: {str(e)}")

    @staticmethod
    def serialize_keys(private_key, public_key, private_path, public_path):
        """
        Serializes RSA keys to PEM format files

        :param private_key: RSA private key to serialize
        :param public_key: RSA public key to serialize
        :param private_path: File path to save private key
        :param public_path: File path to save public key
        """
        try:
            # serialize private key
            with open(private_path, 'wb') as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            # serialize public key
            with open(public_path, 'wb') as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))
        except Exception as e:
            raise Exception(f"Error at serialize keys: {str(e)}")

    @staticmethod
    def encrypt_symmetric_key(symmetric_key, public_key, output_path):
        """
        Encrypts symmetric key with RSA public key and saves to file

        :param symmetric_key: Symmetric key to encrypt
        :param public_key: RSA public key for encryption
        :param output_path: File path to save encrypted key
        """
        try:
            encrypted_key = public_key.encrypt(
                symmetric_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            with open(output_path, 'wb') as f:
                pickle.dump(encrypted_key, f)
        except Exception as e:
            raise Exception(f"Error at encryption symmetric key: {str(e)}")

    def generate_save_keys(self, encrypted_sym_key_path,
                           public_key_path, private_key_path):
        """
        Complete key generation and saving workflow

        :param encrypted_sym_key_path: Path to save encrypted symmetric key
        :param public_key_path: Path to save public RSA key
        :param private_key_path: Path to save private RSA key
        :return:
        """
        try:
            # generate sym key
            sym_key = self.generate_symmetric_key()

            # generate asym keys
            private_key, public_key = self.generate_asymmetric_key()

            # serialize asym keys
            self.serialize_keys(private_key, public_key,
                                private_key_path, public_key_path)

            # encrypt sym keys
            self.encrypt_symmetric_key(sym_key, public_key,
                                       encrypted_sym_key_path)

            print("All keys generated and saved successfully")
        except Exception as e:
            raise Exception(f"Error in generation process: {str(e)}")

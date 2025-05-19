import os
import pickle

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class Encryptor:
    def __init__(self):
        self.backend = default_backend()

    def decrypt_symmetric_key(self, encrypted_key_path, private_key_path):
        """

        :param encrypted_key_path:
        :param private_key_path:
        :return:
        """
        try:
            with open(private_key_path, 'rb') as f:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=self.backend
                )

            with open(encrypted_key_path, 'rb') as f:
                encrypted_key = pickle.load(f)

            symmetric_key = private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return symmetric_key
        except Exception as e:
            raise Exception(f"Error at decrypting key: {str(e)}")

    def encrypt_file(self, input_file_path, output_file_path, symmetric_key):
        """

        :param input_file_path:
        :param output_file_path:
        :param symmetric_key:
        :return:
        """
        try:
            iv = os.urandom(16)

            cipher = Cipher(
                algorithms.Camellia(symmetric_key),
                modes.CBC(iv),
                backend=self.backend
            )
            encryptor = cipher.encryptor()

            with open(input_file_path, 'rb') as infile, open(output_file_path, 'wb') as outfile:
                outfile.write(iv)

                while True:
                    chunk = infile.read(4096)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.update(chunk))
                outfile.write(encryptor.finalize())
        except Exception as e:
            raise Exception(f"Error at encrypting file: {str(e)}")

    def encrypt(self, input_file_path, private_key_path,
                encrypted_key_path, output_file_path):
        """

        :param input_file_path:
        :param private_key_path:
        :param encrypted_key_path:
        :param output_file_path:
        :return:
        """
        try:
            # decrypt sym key
            symmetric_key = self.decrypt_symmetric_key(encrypted_key_path, private_key_path)

            # encrypt file
            self.encrypt_file(input_file_path, output_file_path, symmetric_key)

            print(f"File encrypted and saved successfully in path: {output_file_path}")
        except Exception as e:
            raise Exception(f"Error in encrypting process: {str(e)}")

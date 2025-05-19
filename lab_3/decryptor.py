import pickle

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class Decryptor:
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

    def decrypt_file(self, input_file_path, output_file_path, symmetric_key):
        """

        :param input_file_path:
        :param output_file_path:
        :param symmetric_key:
        :return:
        """
        try:
            with open(input_file_path, 'rb') as infile:
                iv = infile.read(16)

                cipher = Cipher(
                    algorithms.Camellia(symmetric_key),
                    modes.CBC(iv),
                    backend=self.backend
                )
                decryptor = cipher.decryptor()

                with open(output_file_path, 'wb') as outfile:
                    while True:
                        chunk = infile.read(4096)
                        if len(chunk) == 0:
                            break

                        outfile.write(decryptor.update(chunk))
                    outfile.write(decryptor.finalize())
        except Exception as e:
            raise Exception(f"Error at decrypting file: {str(e)}")

    def decrypt(self, input_file_path, private_key_path,
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

            # decrypt file
            self.decrypt_file(input_file_path, output_file_path, symmetric_key)

            print(f"File decrypted and saved successfully in path:{output_file_path}")
        except Exception as e:
            raise Exception(f"Error in decrypting process: {str(e)}")

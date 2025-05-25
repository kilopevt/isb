from cryptography.hazmat.primitives import serialization

from file_operations import FileManager


class SerializeKeys:
    @staticmethod
    def serialize_private_key(key, path):
        """
        Serializes a private key to PEM format and saves to file

        :param key: Private key object to serialize
        :param path: File path to save the serialized key
        """
        try:
            pem = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            FileManager.write_file(path, pem)
        except Exception as e:
            raise Exception(f"Error at serialization private key: {str(e)}")

    @staticmethod
    def serialize_public_key(key, path):
        """
        Serializes a public key to PEM format and saves to file

        :param key: Public key object to serialize
        :param path: File path to save the serialized key
        """
        try:
            pem = key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            FileManager.write_file(path, pem)
        except Exception as e:
            raise Exception(f"Error at serialization public key: {str(e)}")

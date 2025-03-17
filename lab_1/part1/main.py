import argparse


def read_file(file_path):
    """
    Reads the content of a file and returns the text.

    :param file_path: Path to the file to be read.
    :return: Content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()


def write_file(file_path, text):
    """
    Writes text to a file.

    :param file_path: Path to the file where the text will be written.
    :param text: Text to be written to the file.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)


def parse_arguments():
    """
    Parses command-line arguments and returns them.

    :return: An object containing the command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Encrypting text using the Upgrade Cesar cipher")
    parser.add_argument("text", type=str, help="Text to encrypt")
    parser.add_argument("key", type=str, help="Encryption key")
    parser.add_argument("encrypt_text", type=str, help="Cipher text")
    args = parser.parse_args()
    return args


class UpgradeCesarCipher:
    def __init__(self, key):
        self.key = self.prepare_key(key)

    @staticmethod
    def prepare_key(key):
        """ Prepares the key for use in the cipher. """
        if not all('А' <= char <= 'я' for char in key):
            raise ValueError("Key must consist of russian letters")
        return key.upper()

    @staticmethod
    def shift_char(char, shift):
        """ Shifts a character by a given number of positions in the alphabet. """
        if 'А' <= char <= 'Я':
            start = ord('А')
            return chr(start + (ord(char) - start + shift) % 32)
        elif 'а' <= char <= 'я':
            start = ord('а')
            return chr(start + (ord(char) - start + shift) % 32)
        return char

    def encrypt(self, text):
        """ Encrypts the text using the key. """
        if not text:
            raise ValueError("Text for encrypt can not be empty")

        if not all('А' <= char <= 'я' or char in ' ,.:;!?\n' for char in text):
            raise ValueError("Text must consist of russian letters")

        text = text.upper()
        encrypted_text = []
        key_length = len(self.key)
        key_index = 0

        for char in text:
            if 'А' <= char <= 'я':
                shift = ord(self.key[key_index]) - ord('А')
                encrypted_text.append(self.shift_char(char, shift))
                key_index = (key_index + 1) % key_length
            else:
                encrypted_text.append(char)

        return ''.join(encrypted_text)

    def decrypt(self, decrypt_text):
        """ Decrypts the text using the key. """
        if not decrypt_text:
            raise ValueError("Text for decrypt can not be empty")

        if not all('А' <= char <= 'я' or char in ' ,.:;!?\n' for char in decrypt_text):
            raise ValueError("Decrypt text must consist of russian letters")

        text = decrypt_text.upper()
        decrypted_text = []
        key_length = len(self.key)
        key_index = 0

        for char in text:
            if 'А' <= char <= 'я':
                shift = ord(self.key[key_index]) - ord('А')
                decrypted_text.append(self.shift_char(char, -shift))
                key_index = (key_index + 1) % key_length
            else:
                decrypted_text.append(char)

        return ''.join(decrypted_text)


def main():
    try:
        args = parse_arguments()
        text = read_file(args.text)
        key = read_file(args.key)

        cipher = UpgradeCesarCipher(key)
        encrypted_text = cipher.encrypt(text)

        write_file(args.encrypt_text, encrypted_text)

        print(f"Text encrypted successfully in file '{args.encrypt_text}'")

    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError as e:
        print(f"File not found - {e}")


if __name__ == "__main__":
    main()

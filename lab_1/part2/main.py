import argparse
import configparser
import json


def read_file(file_path):
    """
    Reads the content of a file and returns the text.

    :param file_path: Path to the file to be read.
    :return: Content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()


def read_json(file_path):
    """
    Reads the content of a .json file

    :param file_path: Path to the .json file to be read
    :return: Content of the file
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


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
    parser = argparse.ArgumentParser(description="Decrypting text using frequency analysis")
    parser.add_argument("encrypt_text", type=str, help="Decryption text")
    parser.add_argument("text", type=str, help="Text")
    args = parser.parse_args()
    return args


def char_frequency(text):
    """
    Calculates the frequency of occurrence of each char in the text.

    :param text: source text
    :return: dictionary where key is a symbol, value is frequency of occurrence
    """
    char_count = {}

    for char in text:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

    char_percent = {}
    for char, count in char_count.items():
        char_percent[char] = (count / len(text))

    return char_percent


def decrypt_text(text, key_dict):
    """
    Replace symbols according to the key

    :param text: Text to decrypt
    :param key_dict: dictionary with key
    :return: Decrypted text
    """
    for key, value in key_dict.items():
        text = text.replace(key, value)
    return text


def main():
    try:
        args = parse_arguments()
        text = read_file(args.encrypt_text)

        # char frequency counting
        percent_dict = char_frequency(text)
        sorted_dict = {}
        for key in sorted(percent_dict, key=percent_dict.get, reverse=True):
            sorted_dict[key] = percent_dict[key]
        # print(sorted_dict)

        # read the constant from file
        config = configparser.ConfigParser()
        config.read('consts.txt')
        key_file = config['DEFAULT']['KEY_FILE']
        key = read_json(key_file)

        text = decrypt_text(text, key)

        write_file(args.text, text)

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

import argparse


RUS_FREQUENCY = {
    'о': 0.0965, 'и': 0.0753, 'е': 0.0723, 'а': 0.0648, 'н': 0.0618,
    'т': 0.0616, 'с': 0.0520, 'р': 0.0407, 'в': 0.0393, 'м': 0.0298,

    'л': 0.0294, 'д': 0.0270, 'я': 0.0264, 'к': 0.0260, 'п': 0.0248,
    'з': 0.0160, 'ы': 0.0157, 'ь': 0.0151, 'у': 0.0133, 'ч': 0.0117,

    'ж': 0.0107, 'г': 0.0099, 'х': 0.0087, 'ф': 0.0073, 'й': 0.0069,
    'ю': 0.0067, 'б': 0.0067, 'ц': 0.0050, 'ш': 0.0042, 'щ': 0.0036,
    'э': 0.0024, 'ъ': 0.0004, 'ё': 0.0004, ' ': 0.1287
}


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

        # char replacement
        text = text.replace("Z", " ")
        text = text.replace("E", "И")
        text = text.replace("9", "О")
        text = text.replace("n", "Т")
        text = text.replace("h", "Л")
        text = text.replace("I", "Е")
        text = text.replace("F", "С")
        text = text.replace("x", "Ы")
        text = text.replace("V", "М")
        text = text.replace("A", "Н")
        text = text.replace("B", "Г")
        text = text.replace("W", "У")
        text = text.replace("!", "Р")
        text = text.replace("=", "Д")
        text = text.replace("$", "Ю")
        text = text.replace(">", "Э")
        text = text.replace("C", "А")
        text = text.replace("P", "В")
        text = text.replace("U", "П")
        text = text.replace("S", "Я")
        text = text.replace("t", "Ч")
        text = text.replace("-", "Ь")
        text = text.replace("O", "З")
        text = text.replace("M", "Б")
        text = text.replace("8", "Щ")
        text = text.replace("G", "Х")
        text = text.replace("N", "Т")
        text = text.replace("J", "Ж")
        text = text.replace("L", "Й")
        text = text.replace("R", "Ц")
        text = text.replace("d", "Ш")
        text = text.replace("3", "Ф")
        text = text.replace("Q", "Ё")
        text = text.replace("Y", "Ъ")

        write_file(args.text, text)

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

import math

from scipy.special import gammainc

from consts import *


def write_result(filename, test_name, p_value, conclusion):
    """
    Writes results to a file.

    :param filename: File name to save result
    :param test_name: Test type name
    :param p_value: Numeric value of p_value
    :param conclusion: Test conclusion (passed/failed)
    :return: File with tests results
    """
    try:
        with open(filename, mode='a', encoding="utf-8") as f:
            f.write(f"Test: {test_name}\n")
            f.write(f"P-value: {p_value}\n")
            f.write(f"Conclusion: {conclusion}\n\n")
    except Exception as e:
        print(f"Something went wrong:{e}")


def frequency_test(sequence):
    """
    Performs the frequency (monobit) test for randomness on a binary sequence.

    :param sequence: Binary string to test
    :return: P-value
    """
    length = len(sequence)
    summ = 0.0

    for bit in sequence:
        if bit == '1':
            summ += 1
        else:
            summ -= 1

    summ /= math.sqrt(length)
    p_value = math.erfc(abs(summ) / math.sqrt(2))
    return p_value


def runs_test(sequence):
    """
    Tests for randomness by examining the number of identical consecutive bits.

    :param sequence: Binary string to test
    :return: P-value
    """
    length = len(sequence)
    ones = sequence.count('1')
    zeta = ones / length

    # Checking a precondition
    if abs(zeta - 0.5) >= (2 / math.sqrt(length)):
        return 0.0  # P-value is considered equal to zero

    cosa = 0
    for i in range(length - 1):
        if sequence[i] != sequence[i + 1]:
            cosa += 1

    numerator = abs(cosa - 2 * length * zeta * (1 - zeta))
    denominator = 2 * math.sqrt(2 * length) * zeta * (1 - zeta)
    p_value = math.erfc(numerator / denominator)
    return p_value


def longest_run_test(sequence):
    """
    Analyzes the sequence for long runs of identical bits using block testing.

    :param sequence: Binary string to test
    :return: P-value
    """
    length = len(sequence)
    num_blocks = length // BLOCK_LENGTH
    v = [0, 0, 0, 0]

    for i in range(num_blocks):
        block = sequence[i * BLOCK_LENGTH: (i+1) * BLOCK_LENGTH]
        max_run = 0
        current_run = 0

        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0

        # Block classification
        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    # Calculating Chi-Square
    chi_square = 0.0
    for i in range(4):
        chi_square += ((v[i] - num_blocks * PI[i]) ** 2) / (num_blocks * PI[i])

    # Calculating P-value via Incomplete Gamma Function
    p_value = gammainc(1.5, chi_square / 2)
    return p_value


def tests(sequence, filename):
    """
    Executes all three randomness tests on the given sequence and saves results to file.

    :param sequence: Binary string to test
    :param filename: Output file name for test results
    :return: None
    """
    with open(filename, 'w') as f:
        f.write(f"Testing sequence: {sequence[:20]}...\n\n")

    p_value = frequency_test(sequence)
    conclusion = "Passed" if p_value >= 0.01 else "Failed"
    write_result(filename, "Bit frequency test", p_value, conclusion)

    p_value = runs_test(sequence)
    conclusion = "Passed" if p_value >= 0.01 else "Failed"
    write_result(filename, "Test for identical consecutive bits", p_value, conclusion)

    p_value = longest_run_test(sequence)
    conclusion = "Passed" if p_value >= 0.01 else "Failed"
    write_result(filename, "Test for the longest sequence of ones in a block", p_value, conclusion)


def main():
    try:
        tests(JAVA_SEQUENCE, JAVA_RESULT)
        print(f"Results save to {JAVA_RESULT}")

        tests(CPP_SEQUENCE, CPP_RESULT)
        print(f"Results save to {CPP_RESULT}")
    except Exception as e:
        print(f"Something went wrong:{e}")


if __name__ == "__main__":
    main()

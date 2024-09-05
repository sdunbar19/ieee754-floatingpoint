from BigDecimal import BigDecimal
import random
from tqdm import tqdm

def test_decimal_subtraction():
    bi_test = BigDecimal("100", 32)
    assert bi_test.subtract_decimal_strings("10000", "50") == "9950"
    assert bi_test.subtract_decimal_strings("999999", "999997") == "2"
    assert bi_test.subtract_decimal_strings("56100", "49800") == "6300"
    assert bi_test.subtract_decimal_strings("15677", "5678") == "9999"
    assert bi_test.subtract_decimal_strings("15677", "000005678") == "9999"
    assert bi_test.subtract_decimal_strings("1", "0") == "1"
    assert bi_test.subtract_decimal_strings("1000", "000000") == "1000"
    print("Subtraction unit tests pass")

def test_decimal_addition():
    bi_test = BigDecimal("100", 32)
    assert bi_test.add_decimal_strings("0", "0") == "0"
    assert bi_test.add_decimal_strings("1", "0") == "1"
    assert bi_test.add_decimal_strings("100", "10") == "110"
    assert bi_test.add_decimal_strings("999999999", "1") == "1000000000"
    assert bi_test.add_decimal_strings("999999999", "0000000000000000000000001") == "1000000000"
    assert bi_test.add_decimal_strings("9999", "999") == "10998"
    print("Addition unit tests pass")

def test_decimal_comparison():
    bi_test = BigDecimal("100", 32)
    assert bi_test.compare_decimal_strings("10000", "9999") == 1
    assert bi_test.compare_decimal_strings("9999", "10000") == -1
    assert bi_test.compare_decimal_strings("000009999", "10000") == -1
    assert bi_test.compare_decimal_strings("1000", "1000") == 0
    assert bi_test.compare_decimal_strings("10", "0") == 1
    assert bi_test.compare_decimal_strings("488", "256") == 1
    print("Compare unit tests pass")

def binary_arr_to_str(binary_arr):
    bin_arr_str = "".join([str(e) for e in binary_arr[::-1]])
    while len(bin_arr_str) > 1 and bin_arr_str[0] == "0":
        bin_arr_str = bin_arr_str[1:]
    return bin_arr_str

def test_binary_whole_number_conversion():
    assert binary_arr_to_str(BigDecimal("1000", 11).whole_bin) == "1111101000"
    assert binary_arr_to_str(BigDecimal("1000.125", 11).whole_bin) == "1111101000"
    assert binary_arr_to_str(BigDecimal("256", 11).whole_bin) == "100000000"
    assert binary_arr_to_str(BigDecimal("0000256", 11).whole_bin) == "100000000"
    assert binary_arr_to_str(BigDecimal("0", 11).whole_bin) == "0"
    print("Binary conversion whole number unit tests pass")

def test_binary_decimal_conversion():
    assert binary_arr_to_str(BigDecimal(".125", 10).dec_bin[::-1]) == "100"
    assert binary_arr_to_str(BigDecimal(".5", 10).dec_bin[::-1]) == "1"
    assert binary_arr_to_str(BigDecimal("1.", 10).dec_bin[::-1]) == "0"
    assert binary_arr_to_str(BigDecimal("0.1", 9).dec_bin[::-1]) == "110011000"
    print("Binary conversion decimal unit tests pass")

def test_decimal_comparison_fuzz():
    bi_test = BigDecimal("100", 32)
    for _ in range(1000):
        int1 = str(random.randint(1, 10*40))
        int2 = str(random.randint(0, int(int1) - 1))
        assert bi_test.compare_decimal_strings(int1, int2) == 1
        assert bi_test.compare_decimal_strings(int2, int1) == -1
        assert bi_test.compare_decimal_strings(int1, int1) == 0
        assert bi_test.compare_decimal_strings(int2, int2) == 0
    print("Comparison fuzz tests pass")

def test_decimal_addition_fuzz():
    bi_test = BigDecimal("100", 32)
    for _ in range(1000):
        int1 = str(random.randint(1, 10*40))
        int2 = str(random.randint(0, int(int1) - 1))
        assert bi_test.add_decimal_strings(int1, int2) == str(int(int1) + int(int2))
    print("Addition fuzz tests pass")

def test_decimal_subtraction_fuzz():
    bi_test = BigDecimal("100", 32)
    for _ in range(1000):
        int1 = str(random.randint(1, 10*40))
        int2 = str(random.randint(0, int(int1) - 1))
        assert bi_test.subtract_decimal_strings(int1, int2) == str(int(int1) - int(int2))
    print("Subtraction fuzz tests pass")

def _dummy_dec_bin_to_dec(dec_bin):
    power = len(dec_bin)
    curr = .5
    total = 0
    for i in range(len(dec_bin) - 1, -1, -1):
        total += dec_bin[i] * curr
        curr /= 2
    return total

def assert_within(num1, num2, within):
    assert num1 + within > num2 and num1 - within < num2

def test_binary_conversion_fuzz():
    print("Running conversion tests, please be patient!")
    for _ in tqdm(range(1000)):
        num = random.randint(1, 10**38)
        fractional = random.uniform(0, 1)
        binary = BigDecimal((str(int(num)) + "." + str(fractional)[2:]), 128)
        assert binary_arr_to_str(binary.whole_bin) == bin(num)[2:]
        assert_within(fractional, _dummy_dec_bin_to_dec(binary.dec_bin), 10**-15)
    print("Conversion fuzz tests pass")

test_decimal_subtraction()
test_decimal_addition()
test_decimal_comparison()
test_binary_whole_number_conversion()
test_binary_decimal_conversion()
test_decimal_comparison_fuzz()
test_decimal_addition_fuzz()
test_decimal_subtraction_fuzz()
test_binary_conversion_fuzz()
print("All tests passed!")
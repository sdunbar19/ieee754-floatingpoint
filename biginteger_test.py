from BigInteger import BigInteger
import random

def test_decimal_subtraction():
    bi_test = BigInteger("100", 32)
    assert bi_test._subtract_decimal_strings("10000", "50") == "9950"
    assert bi_test._subtract_decimal_strings("999999", "999997") == "2"
    assert bi_test._subtract_decimal_strings("56100", "49800") == "6300"
    assert bi_test._subtract_decimal_strings("15677", "5678") == "9999"
    assert bi_test._subtract_decimal_strings("1", "0") == "1"
    assert bi_test._subtract_decimal_strings("1000", "0") == "1000"

def test_decimal_comparison():
    bi_test = BigInteger("100", 32)
    assert bi_test._compare_decimal_strings("10000", "9999") == 1
    assert bi_test._compare_decimal_strings("9999", "10000") == -1
    assert bi_test._compare_decimal_strings("1000", "1000") == 0
    assert bi_test._compare_decimal_strings("10", "0") == 1
    assert bi_test._compare_decimal_strings("488", "256") == 1

def binary_arr_to_str(binary_arr):
    bin_arr_str = "".join([str(e) for e in binary_arr[::-1]])
    while len(bin_arr_str) > 1 and bin_arr_str[0] == "0":
        bin_arr_str = bin_arr_str[1:]
    return bin_arr_str

def test_binary_conversion():
    assert binary_arr_to_str(BigInteger("1000", 11).bin_arr) == "1111101000"
    assert binary_arr_to_str(BigInteger("256", 11).bin_arr) == "100000000"

def test_decimal_comparison_fuzz():
    bi_test = BigInteger("100", 32)
    for _ in range(1000):
        int1 = str(random.randint(1, 10*40))
        int2 = str(random.randint(0, int(int1) - 1))
        assert bi_test._compare_decimal_strings(int1, int2) == 1
        assert bi_test._compare_decimal_strings(int2, int1) == -1
        assert bi_test._compare_decimal_strings(int1, int1) == 0
        assert bi_test._compare_decimal_strings(int2, int2) == 0

def test_decimal_subtraction_fuzz():
    bi_test = BigInteger("100", 32)
    for _ in range(1000):
        int1 = str(random.randint(1, 10*40))
        int2 = str(random.randint(0, int(int1) - 1))
        assert bi_test._subtract_decimal_strings(int1, int2) == str(int(int1) - int(int2))

def test_binary_conversion_fuzz():
    for _ in range(1000):
        num = random.randint(1, 10**38)
        binary = BigInteger(str(num), 128)
        assert binary_arr_to_str(binary.bin_arr) == bin(num)[2:]

test_decimal_subtraction()
test_decimal_comparison()
test_binary_conversion()
test_decimal_comparison_fuzz()
test_decimal_subtraction_fuzz()
test_binary_conversion_fuzz()
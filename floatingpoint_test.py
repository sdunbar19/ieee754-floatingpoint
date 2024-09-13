from FloatingPoint import FloatingPoint

def _check_parsing(string, exp_sign, exp_whole, exp_dec):
    fp = FloatingPoint()
    sign, whole, dec = fp._parse_decimal_string(string)
    assert exp_sign == sign
    assert exp_whole == whole
    assert exp_dec == dec

def test_string_parsing():
    _check_parsing("1.000", 0, "1", "000")
    _check_parsing(".123", 0, "", "123")
    _check_parsing("10.0123", 0, "10", "0123")
    _check_parsing("10", 0, "10", "")
    _check_parsing("-1.000", 1, "1", "000")
    print("Decimal parsing unit test pass")

def little_endian_binary_arr_to_big_endian_str(binary_arr):
    bin_arr_str = "".join([str(e) for e in binary_arr[::-1]])
    while len(bin_arr_str) > 1 and bin_arr_str[0] == "0":
        bin_arr_str = bin_arr_str[1:]
    return bin_arr_str

def test_binary_whole_number_conversion():
    fp_test = FloatingPoint()
    assert little_endian_binary_arr_to_big_endian_str(fp_test._whole_num_string_to_binary("1000")) == "1111101000"
    assert little_endian_binary_arr_to_big_endian_str(fp_test._whole_num_string_to_binary("256")) == "100000000"
    assert little_endian_binary_arr_to_big_endian_str(fp_test._whole_num_string_to_binary("0000256")) == "100000000"
    assert little_endian_binary_arr_to_big_endian_str(fp_test._whole_num_string_to_binary("0")) == "0"
    print("Binary conversion whole number unit tests pass")

def _check_decimal_conversion(input_string, least_sig_wn_bit, expected_binary, expected_shift):
    fp_test = FloatingPoint()
    result = fp_test._decimal_string_to_binary(input_string, least_sig_wn_bit)
    assert little_endian_binary_arr_to_big_endian_str(result[0][::-1]) == expected_binary
    assert result[1] == expected_shift

def test_binary_decimal_conversion():
    _check_decimal_conversion("125", -1, "1", 2)
    _check_decimal_conversion("5", -1, "1", 0)
    _check_decimal_conversion("1", -1, "1100110011001100110011", 3)
    _check_decimal_conversion("625", -1, "101", 0)
    _check_decimal_conversion("078125", -1, "101", 3)
    _check_decimal_conversion("078125", 19, "0", 0)
    _check_decimal_conversion("078125", 18, "1000", 0)
    print("Binary conversion decimal unit tests pass")

def _check_binary_against_decimal(bin_array, exp_dec, bias):
    bin_str = "".join([str(x) for x in bin_array])
    assert int(bin_str, 2) == exp_dec + bias

def _test_exponent(msb_whole_num, offset, expected_dec, expected_is_overflow=False, expected_is_underflow=False):
    fp = FloatingPoint()
    fp._populate_exponent(msb_whole_num, offset)
    _check_binary_against_decimal(fp._exponent, expected_dec, fp.bias)
    assert fp._is_overflow == expected_is_overflow
    assert fp._is_underflow == expected_is_underflow

def test_exponent_calculation_population():
    fp_dummy = FloatingPoint()
    _test_exponent(-1, 0, -1)
    _test_exponent(10, 0, 10)
    _test_exponent(fp_dummy.bias, 0, fp_dummy.bias)
    _test_exponent(fp_dummy.bias + 1, 0, fp_dummy.bias + 1, True, False)
    _test_exponent(fp_dummy.bias * 3, 0, fp_dummy.bias + 1, True, False)
    _test_exponent(-1, 10, -11)
    _test_exponent(-1, 40, -41)
    _test_exponent(-1, fp_dummy.bias - 2, -1 * fp_dummy.bias + 1)
    _test_exponent(-1, fp_dummy.bias - 1, -1 * (fp_dummy.bias), False, True)
    _test_exponent(-1, fp_dummy.bias, -1 * (fp_dummy.bias), False, True)
    print("Exponent calculation unit tests pass")

def test_significand_population():
    fp_dummy = FloatingPoint()
    wnum_bin = [0 for _ in range(fp_dummy.significand_bits)]
    dec_bin = [0 for _ in range(fp_dummy.significand_bits)]
    for i in range(10):
        wnum_bin[i] = 1
    for i in range(23):
        dec_bin[i] = 1
    wnum_bin[0] = 0
    dec_bin[9] = 0
    fp_dummy._populate_significand(9, wnum_bin, dec_bin)
    print(fp_dummy._significand)
    for i in range(len(fp_dummy._significand)):
        if i == 8 or i == 22:
            assert fp_dummy._significand[i] == 0
        else:
            assert fp_dummy._significand[i] == 1
    print("Significand population unit tests pass")

def test_floating_point_conversion():
    fp = FloatingPoint()
    fp.initialize("85.125")
    array = fp.get()
    assert "".join([str(x) for x in array]) == "01000010101010100100000000000000"
    print("Floating point conversion tests pass")

test_string_parsing()
test_binary_whole_number_conversion()
test_binary_decimal_conversion()
test_exponent_calculation_population()
test_significand_population()
test_floating_point_conversion()

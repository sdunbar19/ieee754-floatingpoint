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
    if len(bin_arr_str) == 0:
        bin_arr_str = "0"
    while len(bin_arr_str) > 1 and bin_arr_str[0] == "0":
        bin_arr_str = bin_arr_str[1:]
    return bin_arr_str

def _run_binary_whole_number_conversion_test_case(input_str, expected_output_binary_str, expected_shift, is_overflow=False):
    fp_test = FloatingPoint()
    result = fp_test._whole_num_string_to_binary(input_str)
    assert little_endian_binary_arr_to_big_endian_str(result[0]) == expected_output_binary_str
    assert result[1] == expected_shift
    assert fp_test._is_overflow == is_overflow

# incorrect, overflow bound too large
def test_binary_whole_number_conversion():
    _run_binary_whole_number_conversion_test_case("1000", "1111101000", 9)
    _run_binary_whole_number_conversion_test_case("256", "100000000", 8)
    _run_binary_whole_number_conversion_test_case("000256", "100000000", 8)
    _run_binary_whole_number_conversion_test_case("0", "0", -1)
    _run_binary_whole_number_conversion_test_case("4294967296", "100000000000000000000000", 32)
    _run_binary_whole_number_conversion_test_case("170141183460469231731687303715884105728", "100000000000000000000000", 127)
    _run_binary_whole_number_conversion_test_case("340282366920938463463374607431768211456", "0", -1, True)
    _run_binary_whole_number_conversion_test_case("340000000000000000000000000000000000000", "111111111100100110011110", 127)
    _run_binary_whole_number_conversion_test_case("340282346638528859811704183484516925440", "111111111111111111111111", 127)
    _run_binary_whole_number_conversion_test_case("340282346638528859811704183484516925441", "0", -1, True)
    print("Binary conversion whole number unit tests pass")

def _check_decimal_conversion(input_string, most_sig_wn_bit, expected_binary, expected_shift, is_underflow=False):
    fp_test = FloatingPoint()
    result = fp_test._decimal_string_to_binary(input_string, most_sig_wn_bit)
    assert little_endian_binary_arr_to_big_endian_str(result[0][::-1]) == expected_binary
    assert result[1] == expected_shift
    assert fp_test._is_underflow == is_underflow

def test_binary_decimal_conversion():
    _check_decimal_conversion("125", -1, "1", 2)
    _check_decimal_conversion("5", -1, "1", 0)
    _check_decimal_conversion("1", -1, "1100110011001100110011", 3)
    _check_decimal_conversion("625", -1, "101", 0)
    _check_decimal_conversion("078125", -1, "101", 3)
    _check_decimal_conversion("078125", 20, "0", 0)
    _check_decimal_conversion("078125", 19, "1000", 0)
    _check_decimal_conversion("75", -1, "11", 0)
    _check_decimal_conversion("75", 23, "0", 0)
    _check_decimal_conversion("75", 22, "1", 0)
    _check_decimal_conversion("078125", 100, "0", 0)
    _check_decimal_conversion("00390625", -1, "1", 7)
    _check_decimal_conversion("0" * 37 + "11754943508222875079687365372222456778186655567720875215088", -1, "1", 125, False)
    _check_decimal_conversion("0" * 37 + "11754943508222875079687365372222456778186655567720875215087", -1, "0", 126, True)
    _check_decimal_conversion("0" * 99 + "1", -1, "0", 126, True)
    print("Binary conversion decimal unit tests pass")

def _check_binary_against_decimal(bin_array, exp_dec, bias):
    bin_str = "".join([str(x) for x in bin_array])
    assert int(bin_str, 2) == exp_dec + bias

def _test_exponent(msb_whole_num, offset, expected_dec, is_overflow=False, is_underflow=False):
    fp = FloatingPoint()
    fp._is_overflow = is_overflow
    fp._is_underflow = is_underflow
    fp._populate_exponent(msb_whole_num, offset)
    _check_binary_against_decimal(fp._exponent, expected_dec, fp.bias)

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
    _test_exponent(-1, fp_dummy.bias - 1, 0, False, True)
    _test_exponent(-1, fp_dummy.bias, 0, False, True)
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
    for i in range(len(fp_dummy._significand)):
        if i == 8 or i == 22:
            assert fp_dummy._significand[i] == 0
        else:
            assert fp_dummy._significand[i] == 1
    print("Significand population unit tests pass")

def _test_successful_conversion(dec_str, expected_bin_str):
    fp = FloatingPoint()
    fp.initialize(dec_str)
    array = fp.get()
    # print(len(array))
    # print("".join([str(x) for x in array]))
    assert "".join([str(x) for x in array]) == expected_bin_str

# reference -> https://numeral-systems.com/ieee-754-converter/
# since truncation was used, no rounding applied
def test_floating_point_conversion():
    _test_successful_conversion("85.125", "01000010101010100100000000000000")
    _test_successful_conversion("1035.1", "01000100100000010110001100110011")
    _test_successful_conversion("63.02847209", "01000010011111000001110100100111")
    _test_successful_conversion("340000000000000000000000000000000000000", "01111111011111111100100110011110")
    _test_successful_conversion("340282346638528859811704183484516925440", "01111111011111111111111111111111")
    _test_successful_conversion("340282346638528859811704183484516925441", "01111111100000000000000000000000")
    print("Floating point conversion unit tests pass")

test_string_parsing()
test_binary_whole_number_conversion()
test_binary_decimal_conversion()
test_exponent_calculation_population()
test_significand_population()
test_floating_point_conversion()
print("All tests passed!")

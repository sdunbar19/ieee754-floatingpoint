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

def binary_arr_to_str(binary_arr):
    bin_arr_str = "".join([str(e) for e in binary_arr[::-1]])
    while len(bin_arr_str) > 1 and bin_arr_str[0] == "0":
        bin_arr_str = bin_arr_str[1:]
    return bin_arr_str

def test_binary_whole_number_conversion():
    fp_test = FloatingPoint()
    assert binary_arr_to_str(fp_test._whole_num_string_to_binary("1000")) == "1111101000"
    assert binary_arr_to_str(fp_test._whole_num_string_to_binary("256")) == "100000000"
    assert binary_arr_to_str(fp_test._whole_num_string_to_binary("0000256")) == "100000000"
    assert binary_arr_to_str(fp_test._whole_num_string_to_binary("0")) == "0"
    print("Binary conversion whole number unit tests pass")

def _check_decimal_conversion(input_string, least_sig_wn_bit, expected_binary, expected_shift):
    fp_test = FloatingPoint()
    result = fp_test._decimal_string_to_binary(input_string, least_sig_wn_bit)
    assert binary_arr_to_str(result[0][::-1]) == expected_binary
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

def test_floating_point_conversion():
    fp = FloatingPoint()
    fp.initialize("85.125")
    array = fp.get()
    assert "".join([str(x) for x in array]) == "01000010101010100100000000000000"
    print("Floating point conversion tests pass")

test_string_parsing()
test_binary_whole_number_conversion()
test_binary_decimal_conversion()
test_floating_point_conversion()

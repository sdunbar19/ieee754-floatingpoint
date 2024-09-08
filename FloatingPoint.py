from Mode import Mode
from BigInteger import BigInteger

POWERS_OF_TWO_FILE = "powers_of_two.txt"
NUM_POWERS_OF_TWO = 2000

# base is 2
class FloatingPoint():
    def __init__(self):
        self.num_bits = 32
        self.exp_bits = 8
        self.bias = 127
        self.rounding_mode = Mode.ROUND_DOWN # only version supported currently
        self.significand_bits = self.num_bits - self.exp_bits - 1
        self.sign = 0
        self.whole_bin = None
        self.dec_bin = None
        self.is_overflow = False

    def _parse_decimal_string(self, decimal_str):
        length = len(decimal_str)
        sign_bit = 0
        if decimal_str[0] == "-":
            sign_bit = 1
        decimal_idx = sign_bit
        while decimal_idx < length and decimal_str[decimal_idx] != ".":
            decimal_idx += 1
        string_start = sign_bit
        while string_start < len(decimal_str) and decimal_str[string_start] == "0":
            string_start += 1
        whole_num = ""
        if decimal_idx - string_start > 0:
            whole_num = decimal_str[string_start:decimal_idx]
        decimal_num = ""
        if decimal_idx + 1 < length:
            decimal_num = decimal_str[decimal_idx + 1:]
        return sign_bit, whole_num, decimal_num

    # answer is in little endian
    def _whole_num_string_to_binary(self, whole_str):
        whole_bigint = BigInteger(whole_str)
        f = open(POWERS_OF_TWO_FILE)
        f_strings = ["" for _ in range(NUM_POWERS_OF_TWO + 1)]
        i = 0
        for line in f.readlines():
            f_strings[i] = line
            i += 1
        binary = [0 for _ in range(self.significand_bits)]
        curr_bigint = whole_bigint
        for i in range(self.significand_bits - 1, -1, -1):
            binary_string = f_strings[i].strip()
            binary_bigint = BigInteger(binary_string)
            compare = curr_bigint.compare(binary_bigint)
            if compare == 0:
                binary[i] = 1
                break
            elif compare == 1:
                curr_bigint = curr_bigint.subtract(binary_bigint)
                binary[i] = 1
            elif i == self.significand_bits - 1 and compare == 1:
                self.is_overflow = True
                break
        return binary
    
    # decimal string is taken as ."#####"
    # whole part should be omitted
    # result given in little endian, as well as the offset from the answer (for floating small decimals)
    def _decimal_string_to_binary(self, decimal_str, least_sig_wn_bit):
        decimal_range = self.significand_bits - least_sig_wn_bit - 1
        decimal_binary = [0 for _ in range(decimal_range)]
        decimal_places = len(decimal_str)
        decimal_curr = BigInteger(decimal_str)
        if decimal_curr.int_string == "0" or decimal_range == 0:
            return decimal_binary
        is_fixed = least_sig_wn_bit != -1 # we are locked into a whole number
        decimal_i = 0
        actual_i = 0
        while decimal_i < decimal_range:
            decimal_curr = decimal_curr.add(decimal_curr)
            if len(decimal_curr.int_string) > decimal_places:
                decimal_curr = BigInteger(decimal_curr.int_string[1:])
                decimal_binary[decimal_i] = 1
                is_fixed = True
                decimal_i += 1
            elif is_fixed:
                decimal_i += 1
            actual_i += 1
            if decimal_curr.int_string == "0":
                break
        return (decimal_binary[::-1], actual_i - decimal_i)
        
    # Inputs: A decimal string in base 10
    # Outputs: None (initializes object)
    # TODO
    def initialize(self, decimal_str: str):
        sign_bit, whole_num, dec_num = self._parse_decimal_string(decimal_str)
        pass
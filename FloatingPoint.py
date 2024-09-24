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
        self._is_overflow = False
        self._is_underflow = False
        self._sign_bit = 0
        self._significand = [0 for _ in range(self.significand_bits)]
        self._exponent = [0 for _ in range(self.exp_bits)]
        self._float_rep = [0 for _ in range(self.num_bits)]
        self.subnormal_mode = False # TODO: implement subnormals
        self._is_initialized = False

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
    
    def _check_is_overflow(self, f_strings, whole_str):
        largest_value = BigInteger("0")
        for i in range(self.significand_bits + 1):
            shift_i = i + self.bias - self.significand_bits
            large_exp = BigInteger(f_strings[shift_i].strip())
            largest_value = large_exp.add(largest_value)
        if largest_value.compare(BigInteger(whole_str)) == -1:
            self._is_overflow = True
            return True
        return False

    # answer is in little endian
    def _whole_num_string_to_binary(self, whole_str):
        whole_bigint = BigInteger(whole_str)
        f = open(POWERS_OF_TWO_FILE)
        f_strings = ["" for _ in range(NUM_POWERS_OF_TWO + 1)]
        i = 0
        for line in f.readlines():
            f_strings[i] = line
            i += 1
        binary = [0 for _ in range(self.significand_bits + 1)]
        curr_bigint = whole_bigint
        max_exponent = 2**self.exp_bits - 2 - self.bias 
        most_sig_bit = -1
        if not self._check_is_overflow(f_strings, whole_str):
            actual_i = self.significand_bits
            is_fixed = False
            for i in range(max_exponent, -1, -1):
                if actual_i < 0:
                    break
                binary_string = f_strings[i].strip()
                binary_bigint = BigInteger(binary_string)
                compare = curr_bigint.compare(binary_bigint)
                if compare == 0:
                    binary[actual_i] = 1
                    if not is_fixed:
                        most_sig_bit = i
                    break
                elif compare == 1:
                    curr_bigint = curr_bigint.subtract(binary_bigint)
                    binary[actual_i] = 1
                if binary[actual_i] == 1 and not is_fixed:
                    is_fixed = True
                    most_sig_bit = i
                if is_fixed or i < self.significand_bits + 1:
                    actual_i -= 1
        return binary, most_sig_bit
    
    # decimal string is taken as ."#####"
    # whole part should be omitted
    # result given in little endian, as well as the offset from the answer (for floating small decimals)
    def _decimal_string_to_binary(self, decimal_str, most_sig_wn_bit):
        decimal_range = self.significand_bits - most_sig_wn_bit
        decimal_binary = [0 for _ in range(decimal_range)]
        if decimal_range <= 0:
            return [], 0
        decimal_places = len(decimal_str)
        decimal_curr = BigInteger(decimal_str)
        if decimal_curr.int_string == "0" or decimal_range == 0:
            return decimal_binary, 0
        is_fixed = most_sig_wn_bit != -1 # we are locked into a whole number
        decimal_i = 0
        actual_i = 0
        while decimal_i < decimal_range and actual_i < self.bias + self.significand_bits + 1:
            actual_i += 1
            if actual_i == self.bias and not is_fixed:
                self._is_underflow = True
                return [0 for _ in range(decimal_range)], self.bias - 1
            decimal_curr = decimal_curr.add(decimal_curr)
            if len(decimal_curr.int_string) > decimal_places:
                decimal_curr = BigInteger(decimal_curr.int_string[1:])
                decimal_binary[decimal_i] = 1
                is_fixed = True
                decimal_i += 1
            elif is_fixed:
                decimal_i += 1
            if decimal_curr.int_string == "0":
                break
        return (decimal_binary[::-1], actual_i - decimal_i)

    def _populate_exponent(self, most_sig_idx, offset):
        exp = most_sig_idx + -1 * offset
        min_exp = 0 - self.bias + 1
        if self._is_overflow:
            exp = 2**self.exp_bits - 1
        elif self._is_underflow:
            exp = 0
        exp += self.bias
        curr_pot = 2**(self.exp_bits - 1)
        curr = exp
        for i in range(self.exp_bits):
            if curr_pot <= curr:
                curr -= curr_pot
                self._exponent[i] = 1
            curr_pot /= 2

    def _populate_significand(self, most_sig_idx, whole_num_bin, decimal_bin):
        if not self._is_underflow or self._is_overflow:
            curr_significand_bit = 0
            for i in range(min(most_sig_idx, self.significand_bits) - 1, -1, -1):
                self._significand[curr_significand_bit] = whole_num_bin[i]
                curr_significand_bit += 1
            i = len(decimal_bin) - 1
            while i >= 0 and curr_significand_bit < self.significand_bits:
                self._significand[curr_significand_bit] = decimal_bin[i]
                i -= 1
                curr_significand_bit += 1

    def _populate_float_rep(self):
        self._float_rep[0] = self._sign_bit
        for i in range(1, self.exp_bits + 1):
            self._float_rep[i] = self._exponent[i - 1]
        for i in range(self.significand_bits):
            self._float_rep[i + self.exp_bits + 1] = self._significand[i]
        
    # Inputs: A decimal string in base 10
    # Outputs: None (initializes object)
    # TODO
    def initialize(self, decimal_str: str):
        if self._is_initialized:
            raise RuntimeError("Floating point already initialized, please clear to re-initialize")
        sign_bit, whole_num, dec_num = self._parse_decimal_string(decimal_str)

        # get the binary
        whole_num_bin, most_sig_wn_bit = self._whole_num_string_to_binary(whole_num)
        decimal_bin, offset = self._decimal_string_to_binary(dec_num, most_sig_wn_bit)

        self._sign_bit = sign_bit
        self._populate_exponent(most_sig_wn_bit, offset)
        self._populate_significand(most_sig_wn_bit, whole_num_bin, decimal_bin)
        self._populate_float_rep()
        self._is_initialized = True

    def is_initialized(self):
        return self._is_initialized

    def get(self):
        if not self._is_initialized:
            raise RuntimeError("Cannot get float from uninitialized object!")
        return self._float_rep[::]
    
    def clear(self):
        self._is_initialized = False
        self._is_overflow = False
        self._is_underflow = False
        self._sign_bit = 0
        self._significand = [0 for _ in range(self.significand_bits)]
        self._exponent = [0 for _ in range(self.exp_bits)]
        self._float_rep = [0 for _ in range(self.num_bits)]
        
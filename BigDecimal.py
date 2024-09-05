POWERS_OF_TWO_FILE = "powers_of_two.txt"
NUM_POWERS_OF_TWO = 2000

class BigDecimal():
    def __init__(self, decimal_str, max_binary_bits):
        self.num_bits = max_binary_bits
        self.decimal_str = decimal_str
        sign, whole_bin, dec_bin = self._parse_decimal_string(decimal_str, max_binary_bits)
        self.sign = sign
        self.whole_bin = whole_bin
        self.dec_bin = dec_bin
    
    def _parse_decimal_string(self, decimal_str, max_binary_bits):
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
        whole_binary = [0]
        if decimal_idx - string_start > 0:
            whole_num = decimal_str[string_start:decimal_idx]
            whole_binary = self._whole_num_string_to_binary(whole_num, max_binary_bits)
        dec_binary = [0]
        if decimal_idx + 1 < length:
            decimal_num = decimal_str[decimal_idx + 1:]
            dec_binary = self._decimal_string_to_binary(decimal_num, max_binary_bits)
        return sign_bit, whole_binary, dec_binary
    
    def _omit_leading_zeros(self, dec_str):
        str_no_leading = ['' for _ in range(len(dec_str))]
        curr = 0
        for i in range(len(dec_str)):
            if curr != 0 or dec_str[i] != '0':
                str_no_leading[curr] = dec_str[i]
                curr += 1
        res = ''.join(str_no_leading)
        if res == '':
            return "0"
        return res

    # answer is in little endian
    def _whole_num_string_to_binary(self, whole_str, max_binary_bits):
        whole_str = self._omit_leading_zeros(whole_str)
        f = open(POWERS_OF_TWO_FILE)
        f_strings = ["" for _ in range(NUM_POWERS_OF_TWO + 1)]
        i = 0
        for line in f.readlines():
            f_strings[i] = line
            i += 1
        binary = [0 for _ in range(max_binary_bits)]
        curr_string = whole_str
        for i in range(max_binary_bits - 1, -1, -1):
            binary_string = f_strings[i].strip()
            compare = self.compare_decimal_strings(curr_string, binary_string) 
            if compare == 0:
                binary[i] = 1
                break
            elif compare == 1:
                curr_string = self.subtract_decimal_strings(curr_string, binary_string)
                binary[i] = 1
        return binary
    
    # decimal string is taken as ."#####""
    # whole part should be omitted
    # result given in little endian, divide by 2^#bits
    def _decimal_string_to_binary(self, decimal_str, max_binary_bits):
        decimal_binary = [0 for _ in range(max_binary_bits)]
        decimal_places = len(decimal_str)
        decimal_no_zeros = self._omit_leading_zeros(decimal_str)
        if decimal_no_zeros == "0":
            return decimal_binary
        i = 0
        for i in range(max_binary_bits):
            decimal_doubled = self.add_decimal_strings(decimal_no_zeros, decimal_no_zeros)
            if len(decimal_doubled) > decimal_places:
                decimal_doubled = decimal_doubled[1:]
                decimal_binary[i] = 1
            else:
                decimal_binary[i] = 0
            decimal_no_zeros = self._omit_leading_zeros(decimal_doubled)
            if decimal_no_zeros == "0":
                break
        return decimal_binary[::-1]
    
    # whole numbers only
    def compare_decimal_strings(self, string1, string2):
        string1 = self._omit_leading_zeros(string1)
        string2 = self._omit_leading_zeros(string2)
        if len(string1) > len(string2):
            return 1
        if len(string1) < len(string2):
            return -1
        for i in range(len(string1)):
            if int(string1[i]) > int(string2[i]):
                return 1
            if int(string1[i]) < int(string2[i]):
                return -1
        return 0

    # bigger should be bigger
    # strings should not be equal
    # whole numbers only
    def subtract_decimal_strings(self, bigger, smaller):
        borrow = 0
        bigger = self._omit_leading_zeros(bigger)
        smaller = self._omit_leading_zeros(smaller)
        result = ['' for _ in range(len(bigger))]
        for i in range(len(smaller) - 1, -1, -1):
            result_i = i + len(bigger) - len(smaller)
            bigger_digit = int(bigger[result_i].strip())
            smaller_digit = int(smaller[i].strip())
            if bigger_digit - smaller_digit - borrow >= 0:
                result[result_i] = str(bigger_digit - smaller_digit - borrow)
                borrow = 0
            else:
                bigger_digit += 10
                result[result_i] = str(bigger_digit - smaller_digit - borrow)
                borrow = 1
        for i in range(len(bigger) - len(smaller) - 1, -1, -1):
            if borrow == 0:
                result[i] = bigger[i]
            else:
                if int(bigger[i]) > 0:
                    result[i] = str(int(bigger[i]) - 1)
                    borrow = 0
                else:
                    result[i] = '9'
        result_no_leading = ['' for _ in range(len(bigger))]
        curr = 0
        for i in range(len(result)):
            if curr != 0 or result[i] != '0':
                result_no_leading[curr] = result[i]
                curr += 1
        return "".join(result_no_leading)
    
    # bigger should be >= smaller
    # whole numbers only
    def add_decimal_strings(self, bigger, smaller):
        bigger = self._omit_leading_zeros(bigger)
        smaller = self._omit_leading_zeros(smaller)
        carry = 0
        result = ['' for _ in range(len(bigger))]
        for i in range(len(smaller) - 1, -1, -1):
            result_i = len(result) - len(smaller) + i
            added = int(bigger[result_i]) + int(smaller[i]) + carry
            if added >= 10:
                carry = 1
                added -= 10
            else:
                carry = 0
            result[result_i] = str(added)
        for i in range(len(bigger) - len(smaller) - 1, -1, -1):
            added = int(bigger[i]) + carry
            if added == 10:
                carry = 1
                added -= 10
            else:
                carry = 0
            result[i] = str(added)
        if carry == 1:
            result_new = [0 for _ in range(len(bigger) + 1)]
            result_new[0] = "1"
            for i in range(len(bigger)):
                result_new[i + 1] = result[i]
            result = result_new
        return "".join(result)

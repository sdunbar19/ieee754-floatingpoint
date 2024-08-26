POWERS_OF_TWO_FILE = "powers_of_two.txt"
NUM_POWERS_OF_TWO = 2000

class BigInteger():
    def __init__(self, decimal_str, max_binary_bits):
        self.num_bits = max_binary_bits
        self.decimal_str = decimal_str
        self.bin_arr = self._constructor_str_to_binary(decimal_str, max_binary_bits)
    
    # decimal string should have no leading 0s
    # answer is in little endian
    def _constructor_str_to_binary(self, decimal_str, max_binary_bits):
        f = open(POWERS_OF_TWO_FILE)
        f_strings = ["" for _ in range(NUM_POWERS_OF_TWO + 1)]
        i = 0
        for line in f.readlines():
            f_strings[i] = line
            i += 1
        binary = [0 for _ in range(max_binary_bits)]
        curr_string = decimal_str
        for i in range(max_binary_bits - 1, -1, -1):
            binary_string = f_strings[i].strip()
            compare = self._compare_decimal_strings(curr_string, binary_string) 
            if compare == 0:
                binary[i] = 1
                break
            elif compare == 1:
                curr_string = self._subtract_decimal_strings(curr_string, binary_string)
                binary[i] = 1
        return binary
    
    # neither string should have leading 0s
    def _compare_decimal_strings(self, string1, string2):
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

    # neither string should have leading 0s unless they are 0
    # bigger should be bigger
    # strings should not be equal
    def _subtract_decimal_strings(self, bigger, smaller):
        borrow = 0
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

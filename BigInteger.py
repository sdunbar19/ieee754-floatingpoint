class BigInteger():
    def __init__(self, int_string):
        self.int_string = self._omit_leading_zeros(int_string)

    def _omit_leading_zeros(self, int_str):
        str_no_leading = ['' for _ in range(len(int_str))]
        curr = 0
        for i in range(len(int_str)):
            if curr != 0 or int_str[i] != '0':
                str_no_leading[curr] = int_str[i]
                curr += 1
        res = ''.join(str_no_leading)
        if res == '':
            return "0"
        return res

    def compare(self, other_bi):
        string1 = self.int_string
        string2 = other_bi.int_string
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

    # should be > argument
    # whole numbers only
    def subtract(self, smaller_bi):
        borrow = 0
        bigger = self.int_string
        smaller = smaller_bi.int_string
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
        return BigInteger("".join(result_no_leading))
    
    # should be >= argument
    # whole numbers only
    def add(self, le_bi):
        bigger = self.int_string
        smaller = le_bi.int_string
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
        return BigInteger("".join(result))

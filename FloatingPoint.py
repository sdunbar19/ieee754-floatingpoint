from Mode import Mode

# base is 2
class FloatingPoint():
    def __init__(self):
        self.num_bits = 32
        self.exp_bits = 8
        self.binary_array = [0 for _ in range(self.num_bits)]
        self.bias = 127
        self.rounding_mode = Mode.ROUND_NEAREST_TIES_EVEN # only version supported currently
        self.significand_bits = self.num_bits - self.exp_bits - 1

    def _convert_decimal_string_to_binary(self, decimal: str, length: str):
        pass
    
    # Inputs: A decimal string in base 10
    # Outputs: None (initializes object)
    def initialize(self, decimal: str, length: int):
        # 1. figure out sign
        # 2. figure out whole number and convert to base 2 - handle if too large or too small
        # 3. figure out decimal and convert to base 2
        # 4. if decimal too long, round
        # 5. figure out exponent
        # 6. store

        sign_bit = 0
        if decimal[0] == "-":
            sign_bit = 1
        decimal_idx = sign_bit
        while decimal_idx < length and decimal[decimal_idx] != ".":
            decimal_idx += 1

        string_start = sign_bit
        while decimal[string_start] == "0":
            string_start += 1
        if decimal_idx - string_start > 0:
            whole_num = decimal[string_start:decimal_idx]
            whole_part = self._convert_decimal_string_to_binary(decimal, decimal_idx - string_start)


    def get_decimal():
        pass


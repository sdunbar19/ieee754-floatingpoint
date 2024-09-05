from Mode import Mode
from BigDecimal import BigDecimal

# base is 2
class FloatingPoint():
    def __init__(self):
        self.num_bits = 32
        self.exp_bits = 8
        self.bias = 127
        self.rounding_mode = Mode.ROUND_NEAREST_TIES_EVEN # only version supported currently
        self.significand_bits = self.num_bits - self.exp_bits - 1
    
    # Inputs: A decimal string in base 10
    # Outputs: None (initializes object)
    def initialize(self, decimal: str):
        # handle limitations for significand and decimal in terms of bits
        # addition, subtraction (multiplication, division?)
        big_decimal = BigDecimal(decimal, self.num_bits)

    def get_decimal():
        pass


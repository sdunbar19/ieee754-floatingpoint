from BigInteger import BigInteger
import random

def _assert_sub(bigger, smaller):
    assert int(BigInteger(bigger).subtract(BigInteger(smaller)).int_string) == int(bigger) - int(smaller)

def test_decimal_subtraction():
    _assert_sub("10000", "50")
    _assert_sub("999999", "50")
    _assert_sub("999999", "999997")
    _assert_sub("56100", "49800")
    _assert_sub("15677", "5678")
    _assert_sub("15677", "0000000005678")
    _assert_sub("1", "0")
    _assert_sub("1000", "0")
    _assert_sub("1000", "0000000")
    print("Subtraction unit tests pass")

def _assert_add(bigger, smaller):
    assert int(BigInteger(bigger).add(BigInteger(smaller)).int_string) == int(bigger) + int(smaller)

def test_decimal_addition():
    _assert_add("0", "0")
    _assert_add("00000", "0")
    _assert_add("0", "000000")
    _assert_add("100", "10")
    _assert_add("999999999", "1")
    _assert_add("999999999", "000000000000000000001")
    _assert_add("000000099999999", "1")
    _assert_add("9999", "999")
    print("Addition unit tests pass")

def test_decimal_comparison():
    assert BigInteger("10000").compare(BigInteger("9999")) == 1
    assert BigInteger("9999").compare(BigInteger("10000")) == -1
    assert BigInteger("000009999").compare(BigInteger("10000")) == -1
    assert BigInteger("1000").compare(BigInteger("1000")) == 0
    assert BigInteger("10").compare(BigInteger("0")) == 1
    assert BigInteger("488").compare(BigInteger("256")) == 1
    print("Compare unit tests pass")

def test_decimal_comparison_fuzz():
    for _ in range(1000):
        int1 = BigInteger(str(random.randint(1, 10*40)))
        int2 = BigInteger(str(random.randint(0, int(int1.int_string) - 1)))
        assert int1.compare(int2) == 1
        assert int2.compare(int1) == -1
        assert int1.compare(int1) == 0
        assert int2.compare(int2) == 0
    print("Comparison fuzz tests pass")

def test_decimal_addition_fuzz():
    for _ in range(1000):
        int1 = BigInteger(str(random.randint(1, 10*40)))
        int2 = BigInteger(str(random.randint(0, int(int1.int_string))))
        assert int(int1.add(int2).int_string) == int(int1.int_string) + int(int2.int_string)
    print("Addition fuzz tests pass")

def test_decimal_subtraction_fuzz():
    for _ in range(1000):
        int1 = BigInteger(str(random.randint(1, 10*40)))
        int2 = BigInteger(str(random.randint(0, int(int1.int_string) - 1)))
        assert int(int1.subtract(int2).int_string) == int(int1.int_string) - int(int2.int_string)
    print("Subtraction fuzz tests pass")

test_decimal_subtraction()
test_decimal_addition()
test_decimal_comparison()
test_decimal_comparison_fuzz()
test_decimal_addition_fuzz()
test_decimal_subtraction_fuzz()
print("All tests passed!")
def ConvertBase(num_str, from_base, to_base):
    # Step 1: Convert source string to decimal integer
    decimal_num = int(num_str, from_base)

    # Step 2: Handle special case for zero
    if decimal_num == 0:
        return "0"

    # Step 3: Convert decimal to target base string
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""
    is_negative = decimal_num < 0
    decimal_num = abs(decimal_num)

    while decimal_num > 0:
        result = digits[decimal_num % to_base] + result
        decimal_num //= to_base

    return "-" + result if is_negative else result

# Example: Convert "1A" (Base 16) to Base 8
print(ConvertBase("1A", 16, 8))  # Output: '32'

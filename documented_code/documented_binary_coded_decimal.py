```python
def binary_coded_decimal(number: int) -> str:
    """
    Convert an integer to its Binary Coded Decimal (BCD) representation.

    Parameters:
    number (int): The integer to be converted. Negative numbers are treated as 0 for BCD conversion.

    Returns:
    str: A string representing the BCD of the input number, prefixed with '0b'.

    Example:
    >>> binary_coded_decimal(-2)
    '0b0000'
    >>> binary_coded_decimal(-1)
    '0b0000'
    >>> binary_coded_decimal(0)
    '0b0000'
    >>> binary_coded_decimal(3)
    '0b0011'
    >>> binary_coded_decimal(2)
    '0b0010'
    >>> binary_coded_decimal(12)
    '0b00010010'
    >>> binary_coded_decimal(987)
    '0b100110000111'
    
    Notes:
    - Negative numbers are treated as 0 for BCD conversion.
    - The function returns a string with a '0b' prefix to indicate binary format.
    """
    # Use max(0, number) to handle negative numbers by treating them as 0
    # Convert the number to a string to iterate over each digit
    # For each digit, convert it back to an integer and then to its binary representation
    # Remove the '0b' prefix from the binary string using [2:]
    # Pad the binary string with leading zeros to ensure it is 4 bits long using zfill(4)
    # Join all the binary strings together without any separators
    return "0b" + "".join(
        str(bin(int(digit)))[2:].zfill(4) for digit in str(max(0, number))
    )


if __name__ == "__main__":
    import doctest

    # Run doctest to verify that the examples in the docstring work as expected
    doctest.testmod()
```

### Explanation of Changes:
1. **General Description**: Added a brief description of what the function does and its purpose.
2. **Parameters and Returns**: Detailed explanation of the parameters and return value in the docstring.
3. **Examples**: Provided examples to illustrate how the function works with different inputs.
4. **Notes**: Included notes on how negative numbers are handled and the format of the returned string.
5. **Inline Comments**: Added comments within the code to explain key steps, though they were not requested specifically but can be helpful for clarity.

This documentation should help users understand the purpose and usage of the `binary_coded_decimal` function, as well as how it handles various edge cases.
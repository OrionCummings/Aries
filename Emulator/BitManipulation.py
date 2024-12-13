def bit_mask(index: int) -> int:
    """Returns a 1-bit mask at the specified `index`."""
    return (1 << index)

def set_bit(number: int, index: int) -> int:
    """Sets bit `index` in number `Number`."""
    return number | bit_mask(index)

def get_bit(number: int, index: int) -> int:
    """Gets bit `index` in number `number`."""
    return (number & bit_mask(index)) >> index

def toggle_bit(number: int, index: int) -> int:
    """Toggles bit `index` in number `number`."""
    return (number ^ (1 << (index)))
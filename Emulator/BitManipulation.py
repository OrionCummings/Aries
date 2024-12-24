def bit_mask(start_index: int, end_index: int = None) -> int:
    """Returns a 1-bit mask between the given indices."""
    if end_index is None:
        return (1 << start_index)

    mask = 0
    for i in range(start_index, end_index):
        mask |= (1 << i)

    return mask

def set_bit(number: int, index: int) -> int:
    """Sets bit `index` in number `number`."""
    return number | bit_mask(index)

def get_bit(number: int, index: int) -> int:
    """Gets bit `index` in number `number`."""
    return (number & bit_mask(index)) >> index

def toggle_bit(number: int, index: int) -> int:
    """Toggles bit `index` in number `number`."""
    return (number ^ (1 << (index)))
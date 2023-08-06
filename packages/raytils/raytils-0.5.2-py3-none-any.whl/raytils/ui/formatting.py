

def suffix_join(array: list, sep: str = '', suffix_sep: str = None):
    """Returns similarly to str.join() however allows you to specify a different final join separator

    Example:
        ', '.join(["One", "Two", "Three"])  # => 'One, Two, Three'
        suffix_join(["One", "Two", "Three"], sep=', ', suffix_sep=" or ")  # => 'One, Two or Three'
    """
    if suffix_sep is None:
        suffix_sep = sep
    if len(array) >= 2:
        return sep.join(array[:-1]) + suffix_sep + array[-1]
    return sep.join(array)

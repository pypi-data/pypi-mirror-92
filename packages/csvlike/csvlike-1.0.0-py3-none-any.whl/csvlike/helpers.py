"""
Some helper methods
"""


def make_printable(char):
    """
    Return printable representation of ascii/utf-8 control characters

    :param char: Character to convert to its printable version
    :return str: Printable version of supplied character
    """
    if not len(char):
        return ''
    if len(char) > 1:
        return ''.join(list(map(make_printable, char)))

    codepoint = ord(char)
    if 0x00 <= codepoint <= 0x1f or 0x7f <= codepoint <= 0x9f:
        return chr(0x2400 | codepoint)

    return char if char != ' ' else '·'

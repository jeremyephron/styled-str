"""
This modules implements the Styled class for strings styled with ANSI escape
sequences.

The Styled class is meant to behave in the same logical ways that a string does:
most operations are performed on the content of the string and ignore the 
styling, making formating, iterating, checking containment, etc. behave in a
logical manner.

Other behaviors include the styling information when appropriate, like hashing
and checking equality. This is because it's perfectly sensible to have distinct
strings with the same content but different styles, and they should be treated
as such.
"""

class Styled:
    """
    A Styled string supporting ANSI escape sequence styling.

    Args:
        content (str): the display text.
        fg (str): one of COLORS.
        brightfg (bool): True if fg color should be bright, False otherwise.
        bg (str): one of COLORS.
        brightbg (bool): True if bg color should be bright, False otherwise.
        style (str, list[str]): one or more of STYLES. If one, just the string
            can be provided, otherwise a style must be a list of strings.

    Attributes:
        content (str): the display text.
        codes (list[str]): the ANSI escape sequences used to style the string.
    """

    BASE_FG = 30
    BASE_BG = 40
    BASE_BRIGHT_INC = 60

    COLORS = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan',
              'white')

    STYLES = ('none', 'bold', 'faint', 'italic', 'underlined', 'blink',
              'blink2', 'negative', 'concealed', 'crossed')

    TEMPLATE = "\x1b[{}m{}\x1b[0m"

    def __init__(self, content, fg=None, brightfg=False, bg=None,
                 brightbg=False, style=None):
        self.content = content
        self.codes = []

        if fg:
            self.codes.append(self._color_code(fg, self.BASE_FG
                + (self.BASE_BRIGHT_INC if brightfg else 0)))

        if bg:
            self.codes.append(self._color_code(bg, self.BASE_BG
                + (self.BASE_BRIGHT_INC if brightbg else 0)))

        if style:
            if isinstance(style, str):
                style = [style]
                
            for part in style:
                if part in self.STYLES:
                    self.codes.append(self.STYLES.index(part))
                else:
                    raise ValueError(f"Invalid style '{part}'.")

    def __str__(self):
        return self.TEMPLATE.format(self._join(*self.codes), self.content)

    def __len__(self):
        return len(self.content)

    def __format__(self, format_string):
        return self.TEMPLATE.format(*self.codes,
            self.content.__format__(format_string))

    def __eq__(self, other):
        if not isinstance(other, Styled):
            return False

        return str(self) == str(other)
    
    def __lt__(self, other):
        if not isinstance(other, Styled):
            raise TypeError(f"'<' not supported between instances of "
                            f"'{type(self)}' and '{type(other)}'")

        return str(self) < str(other)

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise TypeError("Styled indices must be integers")

        return self.content[key]

    def __hash__(self):
        return hash(str(self))

    def __nonzero__(self):
        return bool(self.content)

    def __iter__(self):
        return self.content.__iter__()

    def __reversed__(self):
        new = Styled(reversed(self.content))
        new.codes = self.codes
        return new

    def __contains__(self, item):
        return item in self.content

    @staticmethod
    def _color_code(spec, base: int):
        if isinstance(spec, str):
            spec = spec.strip().lower()

        if spec == 'default':
            return Styled._join(base + 9)

        if spec in Styled.COLORS:
            return Styled._join(base + Styled.COLORS.index(spec))

        if isinstance(spec, int) and 0 <= spec <= 255:
            return Styled._join(base + 8, 5, spec)

        if isinstance(spec, (tuple, list)):
            return Styled._join(base + 8, 2, _join(*spec))

    @staticmethod
    def _join(*args):
        return ';'.join(str(arg) for arg in args)


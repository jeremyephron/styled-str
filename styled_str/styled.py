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

import sys
from typing import *


class Styled(str):
    """
    A Styled string supporting ANSI escape sequence styling.

    Args:
        data (str): the display text.
        fg (str): one of COLORS.
        brightfg (bool): True if fg color should be bright, False otherwise.
        bg (str): one of COLORS.
        brightbg (bool): True if bg color should be bright, False otherwise.
        style (str, list[str]): one or more of STYLES. If one, just the string
            can be provided, otherwise a style must be a list of strings.

    Attributes:
        data (str): the display text.
        _codes (list[str]): the ANSI escape sequences used to style the string.
    """

    BASE_FG = 30
    BASE_BG = 40
    BASE_BRIGHT_INC = 60

    COLORS = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan',
              'white')

    STYLES = ('none', 'bold', 'faint', 'italic', 'underlined', 'blink',
              'blink2', 'negative', 'concealed', 'crossed')

    TEMPLATE = "\x1b[{}m{}\x1b[0m"

    def __init__(
        self,
        data: Union[str, 'Styled'],
        /,
        fg: Optional[str] = None,
        brightfg: bool = False,
        bg: Optional[str] = None,
        brightbg: bool = False,
        style: Optional[Union[str, List[str]]] = None
    ) -> None:
        # Set internal data
        if isinstance(data, str):
            self.data = data
        elif isinstance(data, Styled):
            self.data = data.data[:]
        else:
            self.data = str(data)
        
        # Add escape sequence codes for the specified formatting
        self._codes = []

        if fg:
            self._codes.append(self._color_code(
                fg, self.BASE_FG + (self.BASE_BRIGHT_INC if brightfg else 0)
            ))

        if bg:
            self._codes.append(self._color_code(
                bg, self.BASE_BG + (self.BASE_BRIGHT_INC if brightbg else 0)
            ))

        if style:
            if isinstance(style, str):
                style = [style]
                
            for part in style:
                if part in self.STYLES:
                    self._codes.append(self.STYLES.index(part))
                else:
                    raise ValueError(f"Invalid style '{part}'.")


    # TODO
    def __new__(cls, data, codes=None, **kwargs):
        new_styled = super(Styled, cls).__new__(cls, data)
        if codes:
            new_styled._codes = codes[:]
        return new_styled

    def __str__(self):
        """Returns the string including the ansi escape sequences."""

        return self.TEMPLATE.format(self._join(*self._codes), self.data)

    def __repr__(self):
        return repr(self.data)
    
    def __int__(self):
        return int(self.data)

    def __float__(self):
        return float(self.data)

    def __complex__(self):
        return complex(self.data)

    def __hash__(self):
        return hash(self.data)

    def __getnewargs__(self):
        return (self.data, self._codes)
    
    def __eq__(self, other):
        if not isinstance(other, str):
            return False
        elif isinstance(other, Styled):
            return self.data == other.data
        return self.data == other

    def __lt__(self, other):
        if not isinstance(other, str):
            raise TypeError(f"'<' not supported between instances of "
                            f"'{type(self)}' and '{type(other)}'")
        elif isinstance(other, Styled):
            return self.data < other.data
        else:
            return self.data < other

    def __le__(self, other):
        if not isinstance(other, str):
            raise TypeError(f"'<=' not supported between instances of "
                            f"'{type(self)}' and '{type(other)}'")
        elif isinstance(other, Styled):
            return self,data <= other.data
        else:
            return self.data <= other

    def __gt__(self, other):
        if not isinstance(other, str):
            raise TypeError(f"'>' not supported between instances of "
                            f"'{type(self)}' and '{type(other)}'")
        elif isinstance(other, Styled):
            return self,data > other.data
        else:
            return self.data > other
    
    def __ge__(self, other):
        if not isinstance(other, str):
            raise TypeError(f"'>=' not supported between instances of "
                            f"'{type(self)}' and '{type(other)}'")
        elif isinstance(other, Styled):
            return self,data >= other.data
        else:
            return self.data >= other

    def __contains__(self, char):
        if isinstance(char, Styled):
            char = char.data
        return char in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        new_styled = self.__class__(self.data[key])
        new_styled._codes = self._codes[:]
        return new_styled

    def __add__(self, other):
        """Returns a string."""

        if not isinstance(other, str):
            raise TypeError(f"'+' not supported between instances of "
                            f"'{type(self)}' and '{type(other)}'")

        return str(self) + str(other)
    
    def __radd__(self, other):
        """Returns a string."""

        if not isinstance(other, str):
            raise TypeError(f"'+' not supported between instances of "
                            f"'{type(self)}' and '{type(other)}'")

        return str(other) + str(self)
    
    def __mul__(self, n):
        new_styled = self.__class__(self.data * n)
        new_styled._codes = self._codes
        return new_styled

    __rmul__ = __mul__

    def __mod__(self, args):
        new_styled = self.__class__(self.data % args)
        new_styled._codes = self._codes
        return new_styled

    def __rmod__(self, template):
        new_styled = self.__class__(str(template) % self)
        new_styled._codes = self._codes
        return new_styled
    
    def __format__(self, format_string):
        return self.TEMPLATE.format(
            *self._codes, self.data.__format__(format_string)
        )

    ##################
    # String Methods #
    ##################

    def capitalize(self):
        new_styled = self.__class__(self.data.capitalize())
        new_styled._codes = self._codes
        return new_styled

    def casefold(self):
        new_styled = self.__class__(self.data.casefold())
        new_styled._codes = self._codes
        return new_styled

    def center(self, width, *args):
        new_styled = self.__class__(self.data.center(width, *args))
        new_styled._codes = self._codes
        return new_styled

    def count(self, sub, start=0, end=sys.maxsize):
        if isinstance(sub, Styled):
            sub = sub.data
        return self.data.count(sub, start, end)

    def removeprefix(self, prefix, /):
        if isinstance(prefix, Styled):
            prefix = prefix.data
        new_styled = self.__class__(self.data.removeprefix(prefix))
        new_styled._codes = self._codes
        return new_styled

    def removeprefix(self, suffix, /):
        if isinstance(suffix, Styled):
            suffix = suffix.data
        new_styled = self.__class__(self.data.removesuffix(suffix))
        new_styled._codes = self._codes
        return new_styled

    # TODO: What should encode behavior be?
    # def encode(self, encoding='utf-8', errors='strict'):
    #     encoding = 'utf-8' if encoding is None else encoding
    #     errors = 'strict' if errors is None else errors
    #     return self.data.encode(encoding, errors)

    def endswith(self, suffix, start=0, end=sys.maxsize):
        return self.data.endswith(suffix, start, end)

    def expandtabs(self, tabsize=8):
        new_styled = self.__class__(self.data.expandtabs(tabsize))
        new_styled._codes = self._codes
        return new_styled

    def find(self, sub, start=0, end=sys.maxsize):
        if isinstance(sub, Styled):
            sub = sub.data
        return self.data.find(sub, start, end)

    def format(self, /, *args, **kwds):
        return str(self).format(*args, **kwds)

    def format_map(self, mapping):
        return str(self).format_map(mapping)

    def index(self, sub, start=0, end=sys.maxsize):
        return self.data.index(sub, start, end)

    def isalpha(self):
        return self.data.isalpha()

    def isalnum(self):
        return self.data.isalnum()

    def isascii(self):
        return self.data.isascii()

    def isdecimal(self):
        return self.data.isdecimal()

    def isdigit(self):
        return self.data.isdigit()

    def isidentifier(self):
        return self.data.isidentifier()

    def islower(self):
        return self.data.islower()

    def isnumeric(self):
        return self.data.isnumeric()

    def isprintable(self):
        return self.data.isprintable()

    def isspace(self):
        return self.data.isspace()

    def istitle(self):
        return self.data.istitle()

    def isupper(self):
        return self.data.isupper()

    def join(self, seq):
        return str(self).data.join(seq)

    def ljust(self, width, *args):
        new_styled = self.__class__(self.data.ljust(width, *args))
        new_styled._codes = self._codes
        return new_styled

    def lower(self):
        new_styled = self.__class__(self.data.lower())
        new_styled._codes = self._codes
        return new_styled

    def lstrip(self, chars=None):
        new_styled = self.__class__(self.data.lstrip(chars))
        new_styled._codes = self._codes
        return new_styled

    # TODO: What should partition behavior be?
    def partition(self, sep):
        return self.data.partition(sep)

    def replace(self, old, new, maxsplit=-1):
        if isinstance(old, Styled):
            old = old.data
        if isinstance(new, Styled):
            new = new.data
        new_styled = self.__class__(self.data.replace(old, new, maxsplit))
        new_styled._codes = self._codes
        return new_styled
    
    def rfind(self, sub, start=0, end=sys.maxsize):
        if isinstance(sub, Styled):
            sub = sub.data
        return self.data.rfind(sub, start, end)

    def rindex(self, sub, start=0, end=sys.maxsize):
        return self.data.rindex(sub, start, end)

    def rjust(self, width, *args):
        new_styled = self.__class__(self.data.rjust(width, *args))
        new_styled._codes = self._codes
        return new_styled

    # TODO: What should rpartition behavior be?
    def rpartition(self, sep):
        return self.data.rpartition(sep)

    # TODO: What should rsplit behavior be?
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)

    def rstrip(self, chars=None):
        new_styled = self.__class__(self.data.rstrip(chars))
        new_styled._codes = self._codes
        return new_styled

    # TODO: What should split behavior be?
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)

    # TODO: What should splitlines behavior be?
    def splitlines(self, keepends=False):
        return self.data.splitlines(keepends)

    def startswith(self, prefix, start=0, end=sys.maxsize):
        return self.data.startswith(prefix, start, end)

    def strip(self, chars=None):
        new_styled = self.__class__(self.data.strip(chars))
        new_styled._codes = self._codes
        return new_styled

    def swapcase(self):
        new_styled = self.__class__(self.data.swapcase())
        new_styled._codes = self._codes
        return new_styled

    def title(self):
        new_styled = self.__class__(self.data.title())
        new_styled._codes = self._codes
        return new_styled

    def translate(self, *args):
        new_styled = self.__class__(self.data.translate())
        new_styled._codes = self._codes
        return new_styled

    def upper(self):
        new_styled = self.__class__(self.data.upper())
        new_styled._codes = self._codes
        return new_styled

    def zfill(self, width):
        new_styled = self.__class__(self.data.zfill(width))
        new_styled._codes = self._codes
        return new_styled

    ##################
    # Styled Methods #
    ##################

    def copy(self, new_data: Optional[str] = None) -> 'Styled':
        new_styled = self.__class__(new_data if new_data else self.data)
        new_styled._codes = self._codes[:]
        return new_styled

    ##################
    # Static Methods #
    ##################

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


# styled-str
StyledStr is a module for creating strings styled with ANSI escape sequences.
The motivation for writing this package was that many existing string-styling 
modules do not implement logical string behavior, like properly formatting the 
string, indexing, containment, all of which are useless if they don't ignore
the styling.

StyledStr ignores styling and acts on just its content for the following 
operations:

For an example StyledStr `s = StyledStr('Hello!', fg='red', style='italic')`

    - length, e.g. `len(s) => 6`
    - formatting, e.g. `f'{s:.3}' => 'Hel'`
    - indexing, e.g. `s[1] => 'e'`
    - iteration, e.g. `for c in s: => H, e, l, l, o, !`
    - reversed, e.g. `for c in reversed(s): => !, o, l, l, e, H`
    - containment, e.g. only characters of "Hello!" are True for `c in s`
 
We would like to have a strings with the same content viewed as distinct though,
and so StyledStr includes styling for the following operations:

For example StyledStrs `a = StyledStr('Hello!', fg='red'); b = StyledStr('Hello!', bg='blue')`

    - equality, e.g. `a == b => False`
    - comparison, e.g. `a < b => True`
    - hashing, e.g. `hash(a)` not necessarily `hash(b)`

## Installation

Install using pip (Python3):

```
pip3 install styled-str
```

## Usage

Import the module and create a string with your desired styles:

```
from styledstr import Styled

s = Styled('Hello World!', fg='cyan', bg='white', style=['bold', 'underlined'])

# Print it out
print(s)

# Use it in a larger string
print("He said, '" + str(s) + "'")

# Format it worry-free!
print(f'Title: {s:>20}')
```


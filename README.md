# styled-str

styled-str is a package for creating strings styled with ANSI escape sequences.
The motivation for writing this package was that many existing string-styling 
modules do not implement logical string behavior, like properly formatting the 
string, indexing, containment, all of which are useless if they don't ignore
the styling.

The `Styled` object should exhibit logical behavior with respect to all string 
functions.

## Installation

Install using pip (Python3):

```bash
pip3 install styled-str
```

## Usage

Import the module and create a string with your desired styles:

```python
from styled_str import Styled

s = Styled('Hello World! ', fg='cyan', bg='white', style=['bold', 'underlined'])

# Print it out
print(s)

# Use it in a larger string
print("He said, '" + s + "'")

# Format it worry-free!
print(f'Title: {s:>20}')

# String functions logically operate on underlying data
print(s.strip()) # prints styled 'Hello World!'

# ...and much more!
```

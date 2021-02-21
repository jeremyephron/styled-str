import pickle
import tempfile

from styled_str import Styled


def test_int():
    styled = Styled('-123', fg='red', style='underlined')
    assert int(styled) == -123

def test_float():
    styled = Styled('-123.0137', bg='blue', brightbg=True, 
                    style=['underlined', 'blink'])
    assert float(styled) == -123.0137

def test_complex():
    styled = Styled('-2+18.3j', fg='green')
    assert complex(styled) == complex(-2, 18.3)

def test_hash():
    styled_a = Styled('not a string', fg='magenta')
    styled_b = Styled('not a string', bg='black')
    assert hash(styled_a) == hash(styled_b) 

def test_pickle():
    styled = Styled('pickle me!', fg='cyan', bg='white')
    f = tempfile.TemporaryFile()
    pickle.dump(styled, f)
    f.flush()
    f.seek(0)
    loaded = pickle.load(f)
    assert str(styled) == str(loaded)

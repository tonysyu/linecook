from linecook import patterns


def test_any_pattern():
    assert patterns.any_pattern('a', 'b', 'c') == r'(a|b|c)'


def test_bounded_word():
    assert patterns.bounded_word('hello') == r'\bhello\b'


def test_exact_match():
    assert patterns.exact_match('hello') == r'^hello$'

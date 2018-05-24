import re

from .transforms import color_text


PYTHON_KEYWORDS = (
    r"w:(False|class|finally|is|return|None|continue|for|lambda|try|True|def|"
    r"from|nonlocal|while|and|del|global|not|with|as|elif|if|or|yield|assert|"
    r"else|import|pass|break|except|in|raise)"
)

SINGLE_QUOTED_STRINGS = "'[^']*'"
DOUBLE_QUOTED_STRINGS = '"[^"]*"'
STRINGS = '({}|{})'.format(SINGLE_QUOTED_STRINGS, DOUBLE_QUOTED_STRINGS)


LINECOOK_CONFIG = {
    'recipes': {
        'default': [],
        'python': [
            color_text(PYTHON_KEYWORDS, 'red'),
            color_text(STRINGS, 'yellow'),
        ],
    },
}

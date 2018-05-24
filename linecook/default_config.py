from . import patterns
from .transforms import color_text


PYTHON_KEYWORDS = (
    r"w:(False|class|finally|is|return|None|continue|for|lambda|try|True|def|"
    r"from|nonlocal|while|and|del|global|not|with|as|elif|if|or|yield|assert|"
    r"else|import|pass|break|except|in|raise)"
)


LINECOOK_CONFIG = {
    'recipes': {
        'default': [],
        'python': [
            color_text(PYTHON_KEYWORDS, 'red'),
            color_text(patterns.strings, 'yellow'),
        ],
    },
}

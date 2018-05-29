from toolz.functoolz import compose

from . import patterns
from .transforms import color_text, partition


PYTHON_KEYWORDS = (
    r"w:(False|class|finally|is|return|None|continue|for|lambda|try|True|def|"
    r"from|nonlocal|while|and|del|global|not|with|as|elif|if|or|yield|assert|"
    r"else|import|pass|break|except|in|raise)"
)


LINECOOK_CONFIG = {
    'recipes': {
        'default': [],
        'python': [
            partition(
                patterns.strings,
                on_match_success=color_text('.*', 'yellow'),
                on_match_failure=compose(
                    color_text(PYTHON_KEYWORDS, 'red'),
                    color_text(patterns.number, 'cyan'),
                ),
            ),
        ],
    },
}

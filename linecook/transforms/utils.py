import functools

from ..parsers import resolve_match_pattern


def match_pattern_transform(func):
    """Decorator transforming a text transform into factory function.

    This should be used to decorate functions that expect a string to transform
    as the first argument and a match pattern as a second argument (see
    `linecook.parsers.resolve_match_pattern` for details on match patterns).
    The decorated function will be a factory function where the output is
    a function that operates solely on text.

    This is used for functions that you want to initialize with a match pattern
    (and possibility other configuration) and use multiple times on text.

    Examples:

    >>> @match_pattern_transform
    ... def replace_text(string, match_pattern, replacement):
    ...     return match_pattern.sub(replacement, string)
    ...
    >>> verbose_thanks = replace_text('Thx', 'Thanks')
    >>> print(verbose_thanks('Thx for the memories'))
    Thanks for the memories
    >>> print(verbose_thanks("You're the best! Thx!"))
    You're the best! Thanks!

    Note that the match pattern was defined as the second argument, but the
    resulting function is called with the pattern as the first argument.
    """
    @functools.wraps(func)
    def wrapped(match_pattern, *args, **kwargs):
        match_pattern = resolve_match_pattern(match_pattern)

        def transform(string):
            return func(string, match_pattern, *args, **kwargs)
        return transform

    return wrapped

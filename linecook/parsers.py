import re


def name_regex(name, pattern):
    """Return regex string as a named capture group."""
    return r'(?P<{name}>{pattern})'.format(name=name, pattern=pattern)


def named_regexes(**names_and_patterns):
    """Return dictionary with regexes transformed into named capture groups.
    """
    return {k: name_regex(k, p) for k, p in names_and_patterns.items()}


def match_regex_template(string, template, **keys_and_patterns):
    """Return dictionary of matches.

    Parameters
    ----------
    string : str
        String containing desired data.
    template : str
        Template string with named fields.
    keys_and_patterns : str
        Regexes for each field in the template.
    """
    named_patterns = named_regexes(**keys_and_patterns)
    pattern = template.format(**named_patterns)

    match = re.search(pattern, string)
    if match is None:
        raise RuntimeError(error_message.format(string=string,
                                                template=template,
                                                pattern=pattern))
    return match.groupdict()

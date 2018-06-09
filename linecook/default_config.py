from . import recipes


LINECOOK_CONFIG = {
    'recipes': {
        'identity': [],  # Recipe that does noting; useful for testing.
        'default': [],

        'python': recipes.python.recipe,
        'dpkg.log': recipes.dpkg_log.recipe,
    },
}

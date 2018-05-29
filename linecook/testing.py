class IdentityMock:

    def __init__(self, template='{}'):
        self.calls = []
        self.template = template

    def __call__(self, string):
        self.calls.append(string)
        return self.template.format(string)

    def assert_called_once_with(self, *args, **kwargs):
        if len(self.calls) != 1:
            msg = "Expected single call but found {}"
            raise AssertionError(msg.format(self.calls))

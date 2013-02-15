#FAKE implementation of interfaces


class FakeSchema(object):
    def __init__(self):
        self.fields = []

    def __getitem__(self, key):
        return self.fields[key]

fake_schema = FakeSchema()


class FakeField(object):
    def __init__(self, default):
        self.default = default


class FakeConfigurableView(object):
    jsvarname = "jsvarname"

    settings_schema = fake_schema
    settings_providers = ('myprovider',)
    settings_mutator = 'mymutator'

    def __init__(self):
        self.context = FakeContext()
        self.request = None
        self.settings = {}

    def settings_javascripts(self):
        return ''


class FakeConfigurationProvider(object):
    def __init__(self):
        self.configuration = {'foo': 'bar'}

    def get(self):
        return self.configuration


class FakeConfigurationMutator(FakeConfigurationProvider):
    def set(self, configuration):
        self.configuration = configuration


class FakeContext(object):

    def __init__(self):
        self.id = "myid"
        self.title = "a title"
        self.aq_inner = self


class FakeRegistry(object):
    def __init__(self):
        self.configuration = {}

    def forInterface(self, schema, check=True):
        class Proxy:
            def __init__(self):
                self.foo = 'bar'
                self.boo = 'far'
        return Proxy()

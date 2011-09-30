#FAKE implementation of interfaces

class FakeField(object):
    def __init__(self, name, default):
        self.default = default
        self.name = None

class FakeSchema(object):

    def __init__(self):
        self.fields = []
        self.iterator = iter([])
        self.addField('foo', 'bar')
        self.addField('boo', 'far')

    def __getitem__(self, key):
        for field in self.fields:
            if field.name == key:
                return field
        raise KeyError(key)

    def __iter__(self):
        return self.iterator

    def next(self):
        return self.iterator.next()

    def addField(self, name, default):
        field = FakeField(name, default)
        self.fields.append(field)
        self.iterator = iter([field.name for field in self.fields])


class FakeConfigurableView(object):
    jsvarname = "jsvarname"

    settings_schema = FakeSchema()

    def __init__(self):
        self.context = FakeContext()
        self.request = None
        self.settings = {}
        
    def settings_javascripts(self):
        return ''

class FakeContext(object):

    def __init__(self):
        self.id = "myid"
        self.title = "a title"
        self.aq_inner = self

class FakeRegistry(object):
    def __init__(self):
        self.configuration = {}
    
    def forInterface(self, schema,check=True):
        class Proxy:
            def __init__(self):
                self.foo = 'bar'
                self.boo = 'far'
        return Proxy()

class UrlParser:
    regex = '[0-9]{4}'

    @classmethod
    def to_python(self, value):
        return int(value)

    @classmethod
    def add_int(self, url, value):
        return url+value
    
    @classmethod
    def add_str(self, url, value):
        return url+('%04d' % value)
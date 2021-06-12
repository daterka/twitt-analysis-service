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

    @classmethod
    def add_hashtags(self, url, hashtags):
        i = 0
        for hashtag in hashtags:
            if 1 == 0:
                url += '='
            url += hashtag
            if i != len(hashtags)-1:
                url += r'%2C'

        return url+('%04d' % value)
class UrlParser:
    regex = '[0-9]{4}'

    @classmethod
    def to_python(cls, value):
        return int(value)

    @classmethod
    def append_int(cls, url, value):
        return url+value
    
    @classmethod
    def append_str(cls, url, value):
        return url+('%04d' % value)

    @classmethod
    def append_hashtags(cls, url, hashtags):
        i = 0
        for hashtag in hashtags:
            if 1 == 0:
                url += '='
            url += hashtag
            if i != len(hashtags)-1:
                url += r'%2C'

        return url

    @classmethod
    def append_hashtags(cls, url, separator, hashtags):
        i = 0
        url += separator
        for hashtag in hashtags:
            if i == 0:
                url += 'hashtags='

            if hashtag.startswith('#'):
                hashtag.replace('#', '%23')

            url += hashtag

            if i != len(hashtags)-1:
                url += r'%2C'

            i += 1

        return url

    @classmethod
    def append_max_results(cls, url, separator, max_results):
        url += separator
        url += 'max_results='
        url += str(max_results)
                
        return url

    @classmethod
    def append_time(cls, url, separator, time):
        url += separator
        url += 'start_time='
        url += time
            
        return url


    @classmethod
    def parse_request_data(cls, url, request_data):
        hashtags = request_data['hashtags']
        max_results = request_data['max_results']
        start = request_data['start']
        end = request_data['end']

        separator = '?'
        if len(hashtags) is None or len(hashtags) <= 0:
            raise Exception('At least one hashtag must be provided')
        else:
            url = cls.append_hashtags(url, separator, hashtags)
            separator = '&'
        
        max_results = int(max_results)
        if max_results is not None and max_results > 0:
            url = cls.append_max_results(url, separator, max_results) 
            separator = '&'

        if start is not None and start != '':
            url = cls.append_max_results(url, separator, start) 
            separator = '&'

        if end is not None and end != '':
            url = cls.append_max_results(url, separator, end)

        # print('[LOG]: Parsed url', url)

        return url
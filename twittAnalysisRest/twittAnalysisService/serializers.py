from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

from twittAnalysisService.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']

from twittAnalysisService.models import PublicMetrics
class PublicMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicMetrics
        fields = ['followers_count', 'following_count', 'tweet_count', 'listed_count']


from django.contrib.auth.validators import UnicodeUsernameValidator
from twittAnalysisService.models import Author
class AuthorSerializer(serializers.ModelSerializer):
    public_metrics = PublicMetricsSerializer()
    class Meta:
        model = Author
        fields = ['username', 'created_at', 'public_metrics', 'id', 'profile_image_url', 'location', 
        'name', 'verified', 'url', 'description', 'protected']
        extra_kwargs = {
            'id': {
                'validators': [UnicodeUsernameValidator()]
            }
        }

    def create(self, validated_data):
        print('\n\nval1: \n', validated_data, '\n\n')
        public_metrics_validated_data = validated_data.pop('public_metrics')
        public_metrics = PublicMetrics.objects.get_or_create(
            followers_count=public_metrics_validated_data.pop('followers_count'),
            following_count=public_metrics_validated_data.pop('following_count'),
            tweet_count=public_metrics_validated_data.pop('tweet_count'),
            listed_count=public_metrics_validated_data.pop('listed_count'))[0]
        
        print('\n\nval2: \n', validated_data, '\n\n')

        author = Author.objects.get_or_create(public_metrics=public_metrics, **validated_data)

        return author

# from twittAnalysisService.models import ReferencedTwitts
# class ReferencedTwittsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ReferencedTwitts
#         fields = ['type', 'id']

from twittAnalysisService.models import Twitt
class TwittSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    # referenced_tweets = ReferencedTwittsSerializer(many=True)
    class Meta:
        model = Twitt
        fields = ['id', 'language', 'conversation_id', 'source', 'created_at', 'author', 'text', 'possibly_sensitive', 
        # 'referenced_tweets', 
        'retweet_count', 'reply_count', 'like_count', 'quote_count', 'annotations', 'mentions', 
        'hashtags', 'cashtags', 'urls']


    def create(self, validated_data):
        author_validated_data = validated_data.pop('author')
        
        public_metrics_validated_data=author_validated_data.pop('public_metrics')
        public_metrics =  PublicMetrics.objects.get_or_create(
            followers_count=public_metrics_validated_data.pop('followers_count'),
            following_count=public_metrics_validated_data.pop('following_count'),
            tweet_count=public_metrics_validated_data.pop('tweet_count'),
            listed_count=public_metrics_validated_data.pop('listed_count'))[0]

        author = Author.objects.get_or_create(
            username=author_validated_data.pop('username'),
            created_at=author_validated_data.pop('created_at'),
            public_metrics=public_metrics,
            id=author_validated_data.pop('id'),
            profile_image_url=author_validated_data.pop('profile_image_url'),
            location=author_validated_data.pop('location'),
            name=author_validated_data.pop('name'),
            verified=author_validated_data.pop('verified'),
            url=author_validated_data.pop('url'),
            description=author_validated_data.pop('description'),
            protected=author_validated_data.pop('protected'))[0]

        twitt_id = validated_data.pop('id')
        twitt = Twitt.objects.get_or_create(
            id = twitt_id,
            author = author,
            **validated_data)[0]

        return twitt
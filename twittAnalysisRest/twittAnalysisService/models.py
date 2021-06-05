from django.db import models

# Create your models here.

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    class Meta:
        ordering = ['created']

class PublicMetrics(models.Model):
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    tweet_count = models.PositiveIntegerField(default=0)
    listed_count = models.PositiveIntegerField(default=0)

class Author(models.Model):
    username = models.CharField(max_length=50, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=False)
    public_metrics = models.ForeignKey(PublicMetrics, on_delete=models.CASCADE)
    id = models.CharField(max_length=20, blank=True, default='', primary_key=True)
    profile_image_url = models.CharField(max_length=100, blank=True, default='')
    location = models.CharField(max_length=20, blank=True, default='')
    name = models.CharField(max_length=20, blank=True, default='')
    verified = models.BooleanField(default=False)
    url = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=200, blank=True, default='')
    protected = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']

class ReferencedTwitts(models.Model):
    type = models.CharField(max_length=20, blank=True, default='')
    twitt_id = models.CharField(max_length=20, blank=True, default='')

class Twitt(models.Model):
    id = models.CharField(max_length=20, blank=True, default='', primary_key=True)
    language = models.CharField(max_length=10, blank=True, default='')
    conversation_id = models.CharField(max_length=20, blank=True, default='')
    source = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=True, default='')
    possibly_sensitive = models.BooleanField(default=False)
    referenced_tweets = []
    retweet_count = models.PositiveIntegerField(default=0)
    reply_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    quote_count = models.PositiveIntegerField(default=0)
    annotations = []
    mentions = []
    hashtags = []
    cashtags = []
    urls = []

    class Meta:
        ordering = ['created_at']

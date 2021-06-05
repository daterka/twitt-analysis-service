from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
# from twittAnalysisService.models import Twitt
from rest_framework import viewsets
from rest_framework import permissions
from twittAnalysisService.serializers import UserSerializer
# from twittAnalysisService.serializers import TwittSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from twittAnalysisService.models import Snippet
from twittAnalysisService.serializers import SnippetSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows snippets to be viewed or edited.
    """
    queryset = Snippet.objects.all().order_by('-created')
    serializer_class = SnippetSerializer
    # permission_classes = [permissions.IsAuthenticated]

csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from twittAnalysisService.models import Twitt
from twittAnalysisService.serializers import TwittSerializer

class TwittViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Twitts to be viewed or edited.
    """
    queryset = Twitt.objects.all().order_by('-created_at')
    serializer_class = TwittSerializer
    # permission_classes = [permissions.IsAuthenticated]

from twittAnalysisService.models import Author
from twittAnalysisService.serializers import AuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Author to be viewed or edited.
    """
    queryset = Author.objects.all().order_by('-created_at')
    serializer_class = AuthorSerializer
    # permission_classes = [permissions.IsAuthenticated]


from twittAnalysisService.models import PublicMetrics
from twittAnalysisService.serializers import PublicMetricsSerializer

class PublicMetricsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows PublicMetricss to be viewed or edited.
    """
    queryset = PublicMetrics.objects.all().order_by('-id')
    serializer_class = PublicMetricsSerializer
    # permission_classes = [permissions.IsAuthenticated]
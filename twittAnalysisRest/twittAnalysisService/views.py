from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import permissions
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from twittAnalysisService.urlParser import UrlParser
from twittAnalysisService.twittAnalysisService import TwittAnalysisService
import requests

# TWITTS_URL = r'http://agile-stream-75074.herokuapp.com/api/tweets'
TWITTS_URL = r'http://localhost:3000/api/tweets'

@api_view(['GET', 'POST'])
def analyze(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        return Response('Twitt-Analysis-Service is working')

    elif request.method == 'POST':
        if len(request.data) != 0:
            response = requests.get(UrlParser.parse_request_data(TWITTS_URL, request))
            tas = TwittAnalysisService()
            response = tas.analyze(response.content)
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
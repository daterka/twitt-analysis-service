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

TWITTS_URL = r'http://agile-stream-75074.herokuapp.com/api/tweets'

@api_view(['GET', 'POST'])
def analyze(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        return Response('Twitt-Analysis-Service is working')

    elif request.method == 'POST':
        # print('request.data: \n', request.data)
        if len(request.data) != 0:
            # response = requests.get(r'http://agile-stream-75074.herokuapp.com/api/tweets?hashtags=usa%2C%20covid%2C%20wuhan&max_results=100')
            response = requests.get(UrlParser.parse_request_data(TWITTS_URL, request.data))
            # print('response.data: \n', response.content)
            tas = TwittAnalysisService()
            response = tas.analyze(response.content)
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
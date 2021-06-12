from django.urls import path
from twittAnalysisService import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('analyze/aggregate/', views.analyze)
]

urlpatterns = format_suffix_patterns(urlpatterns)
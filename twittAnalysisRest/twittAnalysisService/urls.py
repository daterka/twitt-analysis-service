from django.urls import path
from twittAnalysisService import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # path('snippets/', views.snippet_list),
    # path('snippets/<int:pk>/', views.snippet_detail),
    path('snippets-list/', views.snippet_list2),
    path('snippets-details/<int:pk>/', views.snippet_detail2),
    path('analyze/aggregate/', views.analyze)
]

urlpatterns = format_suffix_patterns(urlpatterns)
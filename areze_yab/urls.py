from django.urls import path

from areze_yab.views import *

urlpatterns = [
    path('diagnostic/', DiagnosticSurveyView.as_view(), name='diagnostic'),
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),
]
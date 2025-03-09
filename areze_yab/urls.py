from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from areze_yab.views import *

urlpatterns = [
    # path('diagnostic/', DiagnosticSurveyView.as_view(), name='diagnostic'),
    path('data/', GetDataAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    # path('request/', send_request, name='request'),
    # path('verify/', verify, name='verify'),
]

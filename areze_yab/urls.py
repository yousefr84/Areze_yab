from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from areze_yab.views import *
from rest_framework.routers import DefaultRouter






urlpatterns = [
    path('company/', CompanyAPIView.as_view(), name='company'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('start-questionnaire/', StartQuestionnaireView.as_view(), name='start-questionnaire'),
    path('questionnaire/<int:questionnaire_id>/answer/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('questionnaire/<int:questionnaire_id>/report/', ReportView.as_view(), name='report'),
    path('questionnaire/<int:questionnaire_id>/status/', QuestionnaireStatusView.as_view(), name='status'),
    path('questionnaires/', QuestionnairesView.as_view(), name='questionnaires'),
    path('domain/',DomainsAPIView.as_view(), name='domain'),
    # path('request/', send_request, name='request'),
    # path('verify/', verify, name='verify'),
    ]

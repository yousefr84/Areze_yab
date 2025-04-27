from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from areze_yab.views import *
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'dashboard', HistoryViewSet, basename='history')


urlpatterns = [
    *router.urls,
    path('company/', CompanyAPIView.as_view()),
    path('sales_and_marketing/', SalesAndMarketingAPIView.as_view()),
    path('human_resources/', HumanResourceAPIView.as_view()),
    path("financial/",FinancialAPIVIew.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('branding/', BrandingAPIView.as_view(), name='branding'),
    # path('request/', send_request, name='request'),
    # path('verify/', verify, name='verify'),
    ]

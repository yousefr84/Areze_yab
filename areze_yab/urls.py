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
    path('research_and_development/', ResearchAndDevelopmentAPIView.as_view()),
    path('financial_resources/', FinancialResourcesAPIView.as_view()),
    path('capital_structure/', CapitalStructureAPIView.as_view()),
    path('management_organizational_structure/', ManagementOrganizationalStructureAPIView.as_view()),
    path('customer_relationship_management/', CustomerRelationshipManagementAPIView.as_view()),
    path('manufacturing_and_production/', ManufacturingAndProductionAPIView.as_view()),
    path('product_competitiveness/', ProductCompetitivenessAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    # path('request/', send_request, name='request'),
    # path('verify/', verify, name='verify'),
]

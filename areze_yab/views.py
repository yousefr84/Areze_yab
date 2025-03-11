from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from areze_yab.serializers import *


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        if not data:
            return Response({'error': 'No data provided'}, status=status.HTTP_400_BAD_REQUEST)
        if data['password'] != data['repeatPassword']:
            return Response({'error': 'رمز عبور و تکرار آن با هم برابر نیست'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            if serializer.data['is_company']:
                company = Company.objects.create(name=serializer.data['name'],
                                                 registrationNumber=serializer.data['registrationNumber'],
                                                 nationalID=serializer.data['username'])
                company.user.add(CustomUser.objects.get(id=serializer.data['id']))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyAPIView(APIView):
    def post(self, request):
        userid = request.data['userid']
        company_data = request.data['company']
        if not company_data:
            return Response(data={"error": "Company is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.get(id=userid)
        if not user.is_company:
            company = Company.objects.create(name=company_data['name'],
                                             registrationNumber=company_data['registrationNumber'],
                                             nationalID=company_data['nationalID'])
            company.user.add(user)
            serializer = CompanySerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)


class BaseAPIView(APIView):
    serializer_class = None
    subdomains = None

    def put(self, request):
        nationalID = request.data['nationalID']
        if not nationalID:
            return Response(data={"error": "nationalID is required"}, status=status.HTTP_400_BAD_REQUEST)
        user_id = request.data['userid']
        if not user_id:
            return Response(data={"error": "userid is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(data={"error": "userid does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = Company.objects.get(user=user, nationalID=nationalID)
        except Company.DoesNotExist:
            return Response(data={"error": "Company does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        request.data['company'] = company.id
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        nationalID = request.data['nationalID']
        if not nationalID:
            return Response(data={"error": "nationalID is required"}, status=status.HTTP_400_BAD_REQUEST)
        user_id = request.data['userid']
        if not user_id:
            return Response(data={"error": "userid is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(data={"error": "userid does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            company = Company.objects.get(user=user, nationalID=nationalID)
            company_serializer = CompanySerializer(company)
        except Company.DoesNotExist:
            return Response(data={"error": "Company does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        request.data['company'] = company.id
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        results = {}
        subdomains = self.subdomains
        answers = serializer.validated_data
        for subdomain, fields in subdomains.items():
            values = [answers[field] for field in fields if
                      field in answers and isinstance(answers[field], (int, float))]
            results[subdomain] = sum(values) / len(values) if values else 0

        all_scores = [value for value in answers.values() if isinstance(value, (int, float))]
        results["امتیاز شاخص"] = sum(all_scores) / len(all_scores) if all_scores else 0
        return Response({
            "company": company_serializer.data,
            "results": results
        }, status=status.HTTP_200_OK)



class SalesAndMarketingAPIView(BaseAPIView):
    serializer_class = SalesAndMarketingSerializer
    subdomains = {
        "برندینگ": ["brandIdentity", "visualIdentityActivities", "brandReputationManagement",
                     "brandTrustAndEmotionalConnection"],
        "سهم بازار": ["marketResearchOpportunities", "salesToIndustryRatio", "marketLeadershipPotential"],
        "کانال های توزیع و فروش": ["orderDeliveryTimeliness", "salesNetworkCoverage",
                                         "salesAgencySupervision", "salesRepProductAwareness",
                                         "reliableTransportUsage"],
        "استراتژی فروش و مارکتینگ": ["digitalMarketingUsage", "marketResearchForMarketing",
                                      "marketingPlanningAndGuidelines", "marketingAndSalesNetworking",
                                      "innovativeMarketingUsage", "exhibitionParticipation"],
        "سوابق فروش": ["salesAmountToCostRatio", "salesGrowthLast3Months", "salesToProductionRatio"],
        "شناخت بازار هدف": ["targetMarketDefinition", "marketRegulationsKnowledge",
                                  "competitorAwareness"],
        "فعالیت های صادراتی": ["exportActivitiesAndGlobalMarketUse"]
    }



class HumanResourceAPIView(BaseAPIView):
    parser_classes = HumanResourcesSerializer


class FinancialResourcesAPIView(BaseAPIView):
    serializer_class = FinancialResourcesSerializer


class CapitalStructureAPIView(BaseAPIView):
    serializer_class = CapitalStructureSerializer


class ManagementOrganizationalStructureAPIView(BaseAPIView):
    serializer_class = ManagementOrganizationalStructureSerializer


class CustomerRelationshipManagementAPIView(BaseAPIView):
    serializer_class = CustomerRelationshipManagementSerializer


class ManufacturingAndProductionAPIView(BaseAPIView):
    serializer_class = ManufacturingAndProductionSerializer


class ResearchAndDevelopmentAPIView(BaseAPIView):
    serializer_class = ResearchAndDevelopmentSerializer


class ProductCompetitivenessAPIView(BaseAPIView):
    serializer_class = ProductCompetitivenessSerializer

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
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
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

            print(f"user {userid} is {user}")
            company = Company.objects.create(name=company_data['name'],
                                                registrationNumber=company_data['registrationNumber'],
                                                nationalID=company_data['nationalID'])
            print(f"company created {company}")
            company.user.add(user)
            print(f"user set to {company}")
            serializer = CompanySerializer(company)
            print(f"serializer created {serializer}")
            return Response(serializer.data, status=status.HTTP_200_OK)


class SalesAndMarketingAPIView(APIView):
    def post(self, request):
        pass

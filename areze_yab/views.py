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


class SalesAndMarketingAPIView(APIView):
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
        serializer = SalesAndMarketingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


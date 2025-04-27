from rest_framework import serializers
from areze_yab.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_company=validated_data.get('is_company', False),
            name=validated_data.get('name'),
            registrationNumber=validated_data.get('registrationNumber')
        )
        return user


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class SalesAndMarketingSSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = SalesAndMarketingS
        fields = '__all__'


class SalesAndMarketingMSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = SalesAndMarketingM
        fields = '__all__'


class SalesAndMarketingLSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = SalesAndMarketingL
        fields = '__all__'


class HumanResourcesSSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = HumanResourcesS
        fields = '__all__'


class HumanResourcesMSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = HumanResourcesM
        fields = '__all__'


class HumanResourcesLSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = HumanResourcesL
        fields = '__all__'


class BrandingSSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = BrandingS
        fields = '__all__'


class BrandingMSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = BrandingM
        fields = '__all__'


class BrandingLSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = BrandingL
        fields = '__all__'


class FinancialSerializer(serializers.ModelSerializer):
    Company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    user = UserSerializer(read_only=True)

    class Meta:
        model = Financial
        fields = '__all__'
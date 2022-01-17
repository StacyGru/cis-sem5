from rest_framework import serializers
from .models import (
    Activity,
    City,
    Country,
    Client,
    ClientStatus,
    Contract,
    CurrencyRate,
    Organization,
    EmployeePosition,
    Employee,
    Hotel,
    HotelReservation,
    Passport,
    Payment,
    PreliminaryAgreement,
    TravelRoute,
    Synchronization,
    Trip
)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientStatus
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


class CurrencyRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyRate
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class EmployeePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePosition
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class HotelReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelReservation
        fields = '__all__'


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PreliminaryAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreliminaryAgreement
        fields = '__all__'


class TravelRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelRoute
        fields = '__all__'


class SynchronizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Synchronization
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

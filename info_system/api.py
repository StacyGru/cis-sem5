from rest_framework import viewsets, permissions
from .models import (
    City,
    Client,
    Contract,
    CurrencyRate,
    Employee,
    Hotel,
    HotelReservation,
    Passport,
    Payment,
    PreliminaryAgreement,
    Synchronization,
    Trip
)
from .serializers import (
    CitySerializer,
    ClientSerializer,
    ContractSerializer,
    CurrencyRateSerializer,
    EmployeeSerializer,
    HotelSerializer,
    HotelReservationSerializer,
    PassportSerializer,
    PaymentSerializer,
    PreliminaryAgreementSerializer,
    SynchronizationSerializer,
    TripSerializer
)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CitySerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ClientSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ContractSerializer


class CurrencyRateViewSet(viewsets.ModelViewSet):
    queryset = CurrencyRate.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CurrencyRateSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = EmployeeSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = HotelSerializer


class HotelReservationViewSet(viewsets.ModelViewSet):
    queryset = HotelReservation.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = HotelReservationSerializer


class PassportViewSet(viewsets.ModelViewSet):
    queryset = Passport.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = PassportSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = PaymentSerializer


class PreliminaryAgreementViewSet(viewsets.ModelViewSet):
    queryset = PreliminaryAgreement.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = PreliminaryAgreementSerializer


class SynchronizationViewSet(viewsets.ModelViewSet):
    queryset = Synchronization.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SynchronizationSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TripSerializer

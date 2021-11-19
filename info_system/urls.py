# from rest_framework import routers
from .api import (
    CityViewSet,
    ClientViewSet,
    ClientStatusViewSet,
    ContractViewSet,
    CurrencyRateViewSet,
    OrganizationViewSet,
    EmployeePositionViewSet,
    EmployeeViewSet,
    HotelViewSet,
    HotelReservationViewSet,
    PassportViewSet,
    PaymentViewSet,
    PreliminaryAgreementViewSet,
    SynchronizationViewSet,
    TripViewSet
)
from django.urls import path
from .views import(
    LoginView,
    BaseView,
    ProfileView
)
from django.contrib.auth.views import LogoutView


# router = routers.DefaultRouter()
# router.register('api/city', CityViewSet, 'city')
# router.register('api/client', ClientViewSet, 'client')
# router.register('api/client_status', ClientStatusViewSet, 'client_status')
# router.register('api/contract', ContractViewSet, 'contract')
# router.register('api/currency_rate', CurrencyRateViewSet, 'currency_rate')
# router.register('api/organization', OrganizationViewSet, 'organization')
# router.register('api/employee_position', EmployeePositionViewSet, 'employee_position')
# router.register('api/employee', EmployeeViewSet, 'employee')
# router.register('api/hotel', HotelViewSet, 'hotel')
# router.register('api/hotel_reservation', HotelReservationViewSet, 'hotel_reservation')
# router.register('api/passport', PassportViewSet, 'passport')
# router.register('api/payment', PaymentViewSet, 'payment')
# router.register('api/preliminary_agreement', PreliminaryAgreementViewSet, 'preliminary_agreement')
# router.register('api/synchronization', SynchronizationViewSet, 'synchronization')
# router.register('api/trip', TripViewSet, 'trip')
urlpatterns = [
    # router.urls
    path('', BaseView.as_view(), name='main'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile')
]
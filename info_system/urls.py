from rest_framework import routers
from .api import (
    CityViewSet,
    ClientViewSet,
    ContractViewSet,
    CurrencyRateViewSet,
    EmployeeViewSet,
    HotelViewSet,
    HotelReservationViewSet,
    PassportViewSet,
    PaymentViewSet,
    PreliminaryAgreementViewSet,
    SynchronizationViewSet,
    TripViewSet
)


router = routers.DefaultRouter()
router.register('api/city', CityViewSet, 'city')
router.register('api/client', ClientViewSet, 'city')
router.register('api/contract', ContractViewSet, 'contract')
router.register('api/currency_rate', CurrencyRateViewSet, 'currency_rate')
router.register('api/employee', EmployeeViewSet, 'employee')
router.register('api/hotel', HotelViewSet, 'hotel')
router.register('api/hotel_reservation', HotelReservationViewSet, 'hotel_reservation')
router.register('api/passport', PassportViewSet, 'passport')
router.register('api/payment', PaymentViewSet, 'payment')
router.register('api/preliminary_agreement', PreliminaryAgreementViewSet, 'preliminary_agreement')
router.register('api/synchronization', SynchronizationViewSet, 'synchronization')
router.register('api/trip', TripViewSet, 'trip')
urlpatterns = router.urls

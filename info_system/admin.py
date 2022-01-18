from django.contrib import admin
from .models import (
    Activity,
    City,
    Client,
    Country,
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
    Trip,
    TransactionLogEmployee
)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'date', 'time', 'day_activity', 'night_activity')
    list_filter = ('user_id', 'date')


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'country')
    list_filter = ('country',)
    search_fields = ('id', 'city')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('id', 'name')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'first_middle_name', 'gender', 'date_of_birth', 'place_of_birth', 'status')
    list_filter = ('gender', 'status')
    search_fields = ('id', 'surname')


class ClientStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time', 'preliminary_agreement_number', 'organization', 'employee', 'trip_participants', 'currency', 'sum')
    list_filter = ('date_time', 'organization', 'employee')
    search_fields = ('id', 'preliminary_agreement_number', 'trip_participants')


class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency_name', 'rate', 'amount')
    search_fields = ('id', 'currency_name')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class EmployeePositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'first_middle_name', 'gender', 'position', 'organization', 'date_of_birth', 'photo', 'user_auth')
    list_filter = ('gender', 'position', 'organization')
    search_fields = ('id', 'surname')


class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'city', 'hotel_name', 'address', 'number_of_stars')
    list_filter = ('country', 'city', 'number_of_stars')
    search_fields = ('id', 'hotel_name', 'address')


class HotelReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'hotel', 'contract_number', 'hotel_room', 'room_type', 'check_in_date', 'check_out_date', 'price')
    list_filter = ('hotel', 'room_type', 'check_in_date', 'check_out_date')
    search_fields = ('id', 'contract_number')


class PassportAdmin(admin.ModelAdmin):
    list_display = ('series', 'number', 'client', 'passport_type', 'date_of_issue', 'expiration_date', 'issued_by')
    list_filter = ('passport_type',)
    search_fields = ('series', 'number', 'client')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time', 'organization', 'contract_number', 'sum_in_rubles')
    list_filter = ('organization', 'date_time')
    search_fields = ('contract_number',)
    readonly_fields = ('sum_in_rubles',)


class PreliminaryAgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time', 'organization', 'employee', 'client', 'number_of_trip_participants', 'country_to_visit', 'trip_start_date', 'trip_end_date')
    list_filter = ('date_time', 'organization', 'employee', 'client')
    search_fields = ('id', 'client')


class TravelRouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'preliminary_agreement_number', 'city_to_visit', 'cities_order', 'hotel_reservation')
    list_filter = ('preliminary_agreement_number',)
    search_fields = ('id', 'city_to_visit', 'cities_order')


class SynchronizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time', 'organization', 'file')
    list_filter = ('date_time', 'organization')
    search_fields = ('date_time',)


class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract_number', 'departure_place', 'arrival_place', 'departure_time', 'arrival_time', 'transport_type', 'transfer', 'travel_document_number', 'currency', 'price')
    list_filter = ('contract_number',)
    search_fields = ('id', 'contract_number')


class TransactionLogEmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'date_time', 'employee_id')


admin.site.register(Activity, ActivityAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(ClientStatus, ClientStatusAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(CurrencyRate, CurrencyRateAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(EmployeePosition, EmployeePositionAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelReservation, HotelReservationAdmin)
admin.site.register(Passport, PassportAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PreliminaryAgreement, PreliminaryAgreementAdmin)
admin.site.register(TravelRoute, TravelRouteAdmin)
admin.site.register(Synchronization, SynchronizationAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(TransactionLogEmployee, TransactionLogEmployeeAdmin)

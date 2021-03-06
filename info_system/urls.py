from django.urls import path
from .views import (
    LoginView,
    MainView,
    ProfileView,
    ClientsView,
    EmployeesView,
    PreliminaryAgreementsView,
    ContractsView,
    PaymentsView,
    ClientsViewOnly,
    EmployeesViewOnly,
    ContractsViewOnly
)
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # ----------------------------------------------- FULL CRUD --------------------------------------------------------
    path('clients/', ClientsView.as_view(), name='clients'),
    path('clients/edit_client/<str:pk>/', views.edit_client, name='edit_client'),
    path('clients/edit_client_passport/<str:pk>/', views.edit_client_passport, name='edit_client_passport'),
    path('clients/add_client_passport/<str:pk>/', views.add_client_passport, name='add_client_passport'),
    path('clients/delete_client/<str:pk>/', views.delete_client, name='delete_client'),
    path('clients/add_client/', views.add_client, name='add_client'),

    path('employees/', EmployeesView.as_view(), name='employees'),
    path('employees/edit_employee/<str:pk>/', views.edit_employee, name='edit_employee'),
    path('employees/delete_employee/<str:pk>/', views.delete_employee, name='delete_employee'),
    path('employees/add_employee/', views.add_employee, name='add_employee'),

    path('preliminary_agreements/', PreliminaryAgreementsView.as_view(), name='preliminary_agreements'),
    path('preliminary_agreements/edit_preliminary_agreement/<str:pk>/', views.edit_preliminary_agreement, name='edit_preliminary_agreement'),
    path('preliminary_agreements/cities_to_visit/cities_to_visit_list/<str:pk>/', views.get_cities_to_visit, name='cities_to_visit_list'),
    path('preliminary_agreements/cities_to_visit/delete_city_to_visit/<str:pk>/', views.delete_city_to_visit, name='delete_city_to_visit'),
    path('preliminary_agreements/cities_to_visit/add_city_to_visit/<str:pk>/', views.add_city_to_visit, name='add_city_to_visit'),
    path('preliminary_agreements/cities_to_visit/choose_country_to_visit/<str:pk>/', views.choose_country_to_visit, name='choose_country_to_visit'),
    path('preliminary_agreements/cities_to_visit/clear_country_to_visit/<str:pk>/', views.clear_country_to_visit, name='clear_country_to_visit'),
    path('preliminary_agreements/delete_preliminary_agreement/<str:pk>/', views.delete_preliminary_agreement, name='delete_preliminary_agreement'),
    path('preliminary_agreements/add_preliminary_agreement/', views.add_preliminary_agreement, name='add_preliminary_agreement'),

    path('contracts/', ContractsView.as_view(), name='contracts'),
    path('contracts/edit_??ontract/<str:pk>/', views.edit_contract, name='edit_contract'),
    path('contracts/hotel_reservations_list/<str:pk>/', views.get_hotel_reservations, name='hotel_reservations_list'),
    path('contracts/hotel_reservations_list/edit_hotel_reservation/<str:pk>/', views.edit_hotel_reservation, name='edit_hotel_reservation'),
    path('contracts/hotel_reservations_list/<str:contract_pk>/add_hotel_reservation/<str:travel_route_pk>/', views.add_hotel_reservation, name='add_hotel_reservation'),
    path('contracts/delete_??ontract/<str:pk>/', views.delete_contract, name='delete_contract'),
    path('contracts/add_??ontract/', views.add_contract, name='add_contract'),

    path('payments/', PaymentsView.as_view(), name='payments'),
    path('payments/currency_rates/', views.currency_rate, name='currency_rates'),
    path('payments/edit_payment/<str:pk>/', views.edit_payment, name='edit_payment'),
    path('payments/delete_payment/<str:pk>/', views.delete_payment, name='delete_payment'),
    path('payments/add_payment/', views.add_payment, name='add_payment'),

    # ------------------------------------------------VIEW ONLY---------------------------------------------------------
    path('view_only/clients/', ClientsViewOnly.as_view(), name='view_only/clients'),
    path('view_only/employees/', EmployeesViewOnly.as_view(), name='view_only/employees'),
    path('view_only/contracts/', ContractsViewOnly.as_view(), name='view_only/contracts'),

]

from django.urls import path
from .views import(
    LoginView,
    MainView,
    ProfileView,
    ClientsView,
    EmployeesView,
    AccountantClientsView,
    AccountantEmployeesView,
    ManagerEmployeesView,
    AgentEmployeesView,
    PreliminaryAgreementsView
)
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # ----------------------------------------------АДМИНИСТРАТОР-------------------------------------------------------
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
    path('preliminary_agreements/delete_preliminary_agreement/<str:pk>/', views.delete_preliminary_agreement, name='delete_preliminary_agreement'),
    path('preliminary_agreements/add_preliminary_agreement/', views.add_preliminary_agreement, name='add_preliminary_agreement'),

    # ------------------------------------------------БУХГАЛТЕР---------------------------------------------------------
    path('accountant/clients/', AccountantClientsView.as_view(), name='accountant/clients'),
    path('accountant/employees/', AccountantEmployeesView.as_view(), name='accountant/employees'),

    # -------------------------------------------------МЕНЕДЖЕР---------------------------------------------------------
    path('manager/employees/', ManagerEmployeesView.as_view(), name='manager/employees'),

    # ---------------------------------------------------АГЕНТ----------------------------------------------------------
    path('agent/employees/', AgentEmployeesView.as_view(), name='agent/employees')

]
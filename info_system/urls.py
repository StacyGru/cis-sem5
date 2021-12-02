from django.urls import path
from .views import(
    LoginView,
    MainView,
    ProfileView,
    ClientsView,
    EmployeesView
)
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('clients/', ClientsView.as_view(), name='clients'),
    path('clients/edit_client/<str:pk>/', views.edit_client, name='edit_client'),
    path('clients/edit_client_passport/<str:pk>/', views.edit_client_passport, name='edit_client_passport'),
    path('clients/add_client_passport/<str:pk>/', views.add_client_passport, name='add_client_passport'),
    path('clients/delete_client/<str:pk>/', views.delete_client, name='delete_client'),
    path('clients/add_client/', views.add_client, name='add_client'),

    path('employees/', EmployeesView.as_view(), name='employees'),
    path('employees/edit_employee/<str:pk>/', views.edit_employee, name='edit_employee'),
    path('employees/delete_employee/<str:pk>/', views.delete_employee, name='delete_employee'),
    path('employees/add_employee/', views.add_employee, name='add_employee')
]
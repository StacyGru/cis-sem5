from django.urls import path
from .views import(
    LoginView,
    MainView,
    ProfileView,
    ClientsView,
    EmployeesView,
    # AddEmployeeView
)
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('clients/', ClientsView.as_view(), name='clients'),
    path('employees/', EmployeesView.as_view(), name='employees'),
    path('employees/edit_employee/<str:pk>/', views.edit_employee, name='edit_employee'),
    path('employees/delete_employee/<str:pk>/', views.delete_employee, name='delete_employee'),
    path('employees/add_employee/', views.add_employee, name='add_employee')
    # path('employees/add_employee/', AddEmployeeView.as_view(), name='add_employee')
]
from django.contrib import messages
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.generic import View
from .forms import (
    LoginForm,
    EmployeeForm
)
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import (
    Client,
    Employee
)
from django.db import transaction


class MainView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'main.html', {})


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/profile')
        return render(request, 'login.html', {'form': form})


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk = request.user.pk)
        return render(
            request,
            'profile.html',
        )


class ClientsView(View):
    def get(self, request, *args, **kwargs):
        clients = Client.objects.all()
        return render(
            request,
            'clients.html',
            {'clients': clients}
        )


class EmployeesView(View):
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        form = EmployeeForm(request.POST or None)
        return render(
            request,
            'employees/employees_list.html',
            {
                'employees': employees,
                'form': form
            }
        )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = EmployeeForm(request.POST or None)
        if form.is_valid():
            new_employee = form.save(commit=False)
            new_employee.surname = form.cleaned_data['surname']
            new_employee.first_middle_name = form.cleaned_data['first_middle_name']
            new_employee.gender = form.cleaned_data['gender']
            new_employee.position = form.cleaned_data['position']
            new_employee.organization = form.cleaned_data['organization']
            new_employee.date_of_birth = form.cleaned_data['date_of_birth']
            new_employee.photo = form.cleaned_data['photo']
            new_employee.save()
            messages.add_message(request, messages.INFO, 'Сотрудник успешно добавлен!')
            return HttpResponseRedirect('/employees')
        messages.add_message(request, messages.ERROR, 'Не удалось добавить сотрудника!')
        return HttpResponseRedirect('/employees')


def edit_employee(request, pk):
    employee = Employee.objects.get(id=pk)
    form = EmployeeForm(instance=employee)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Сотрудник успешно изменён!')
            return HttpResponseRedirect('/employees')
        messages.add_message(request, messages.ERROR, 'Не удалось изменить сотрудника!')
    return render(
        request,
        'employees/edit_employee.html',
        {
            'employee': employee,
            'form': form
        }
    )


def delete_employee(request, pk):
    employee = Employee.objects.get(id=pk)
    if request.method == 'POST':
        employee.delete()
        messages.add_message(request, messages.INFO, 'Сотрудник успешно удалён!')
        return HttpResponseRedirect('/employees')
    return render(
        request,
        'employees/delete_employee.html',
        {
            'employee': employee
        }
    )
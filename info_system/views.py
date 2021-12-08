from django.contrib import messages
from django.db import transaction
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.generic import View
from .forms import (
    LoginForm,
    EmployeeForm,
    ClientForm,
    PassportForm
)
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import (
    Client,
    Employee,
    Passport
)


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
        search_query = request.GET.get('search', '')
        if search_query:
            clients = Client.objects.filter(surname__icontains=search_query) | Client.objects.filter(first_middle_name__icontains=search_query)
        else:
            clients = Client.objects.all()
        return render(
            request,
            'clients/clients_list.html',
            {'clients': clients}
        )


def edit_client(request, pk):
    client = Client.objects.get(id=pk)
    form = ClientForm(instance=client)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Клиент успешно изменён!')
            return HttpResponseRedirect('/clients')
        messages.add_message(request, messages.ERROR, 'Не удалось изменить клиента!')
    return render(
        request,
        'clients/edit_client.html',
        {
            'client': client,
            'form': form
        }
    )


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


def add_client_passport(request, pk):
    form = PassportForm()
    if request.method == 'POST':
        form = PassportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Паспортные данные клиента успешно добавлен!')
            return HttpResponseRedirect('/clients')
        messages.add_message(request, messages.ERROR, 'Не удалось добавить паспортные данные клиента!')
    return render(
            request,
            'clients/add_client_passport.html',
            {
                'form': form
            }
        )


def edit_client_passport(request, pk):
    passport = get_or_none(Passport, client=pk)
    if passport:
        form = PassportForm(instance=passport)
        if request.method == 'POST':
            form = PassportForm(request.POST, instance=passport)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO, 'Клиент успешно изменён!')
                return HttpResponseRedirect('/clients')
            messages.add_message(request, messages.ERROR, 'Не удалось изменить клиента!')
        return render(
            request,
            'clients/edit_client_passport.html',
            {
                'passport': passport,
                'form': form
            }
        )
    else:
        return render(
            request,
            'clients/add_client_passport.html',
        )


def delete_client(request, pk):
    client = Client.objects.get(id=pk)
    if request.method == 'POST':
        client.delete()
        messages.add_message(request, messages.INFO, 'Клиент успешно удалён!')
        return HttpResponseRedirect('/clients')
    return render(
        request,
        'clients/delete_client.html',
        {
            'client': client
        }
    )


def add_client(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        # passport_form = PassportForm()
        if form.is_valid():

            # passport_instance = passport_form.save(commit=False)
            # passport_form.save()
            # client_instance = client_form.save(commit=False)
            # passport_instance.client = client_instance
            # passport_instance.save()

            form.save()
            messages.add_message(request, messages.INFO, 'Клиент успешно добавлен!')
            return HttpResponseRedirect('/clients')
        messages.add_message(request, messages.ERROR, 'Не удалось добавить клиента!')
    return render(
            request,
            'clients/add_client.html',
            {
                'form': form
            }
        )


class EmployeesView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        filters = request.GET.get('employee_position', '')
        if search_query and filters:
            employees = Employee.objects.filter(surname__icontains=search_query) | Employee.objects.filter(first_middle_name__icontains=search_query)
            employees = employees.filter(position=filters)
        elif search_query:
            employees = Employee.objects.filter(surname__icontains=search_query) | Employee.objects.filter(first_middle_name__icontains=search_query)
        elif filters:
            employees = Employee.objects.filter(position=filters)
        else:
            employees = Employee.objects.all()
        return render(
            request,
            'employees/employees_list.html',
            {
                'employees': employees
            }
        )


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


def add_employee(request):
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Сотрудник успешно добавлен!')
            return HttpResponseRedirect('/employees')
        messages.add_message(request, messages.ERROR, 'Не удалось добавить сотрудника!')
    return render(
            request,
            'employees/add_employee.html',
            {
                'form': form
            }
        )

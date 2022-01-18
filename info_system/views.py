import datetime

from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from requests import get
from bs4 import BeautifulSoup as bs
from .forms import (
    LoginForm,
    EmployeeForm,
    ClientForm,
    PassportForm,
    PreliminaryAgreementForm,
    ContractForm,
    CountryToVisitForm,
    CitiesToVisitForm,
    PaymentForm,
    UserActivityForm, AddUserAuthForm, HotelReservationForm
)
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import (
    Client,
    Employee,
    Passport,
    PreliminaryAgreement,
    Contract,
    City,
    TravelRoute,
    Payment,
    CurrencyRate,
    HotelReservation,
    Activity, AuthUser
)


class MainView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'main.html', {}
        )


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
        user = User.objects.get(pk=request.user.pk)
        activities = Activity.objects.filter(user_id=user.id, date=str(datetime.datetime.now().date())).count()
        month_activities_daytime = Activity.objects.filter(user_id=user.id, day_activity=True,
                                                           date__contains='-' + str(
                                                               datetime.datetime.now().date().strftime(
                                                                   '%m')) + '-').count()
        month_activities_nighttime = Activity.objects.filter(user_id=user.id, night_activity=True,
                                                             date__contains='-' + str(
                                                                 datetime.datetime.now().date().strftime(
                                                                     '%m')) + '-').count()
        if month_activities_daytime > month_activities_nighttime:
            status = 'жаворонок'
        elif month_activities_daytime < month_activities_nighttime:
            status = 'сова'
        else:
            status = 'не определился'
        user_id = user.id
        employee = Employee.objects.get(user_auth=request.user.pk)
        return render(
            request,
            'profile.html',
            {
                'user': user,
                'activities': activities,
                'user_id': user_id,
                'status': status,
                'daytime': month_activities_daytime,
                'nighttime': month_activities_nighttime,
                'employee': employee
            }
        )


# ------------------------------------------------- FULL CRUD ----------------------------------------------------------


class ClientsView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        if search_query:
            clients = Client.objects.filter(surname__icontains=search_query) | Client.objects.filter(
                first_middle_name__icontains=search_query)
        else:
            clients = Client.objects.all()
        return render(
            request,
            'full_crud/clients/clients_list.html',
            {'clients': clients}
        )


def edit_client(request, pk):
    client = Client.objects.get(id=pk)
    form = ClientForm(instance=client)
    try:
        passport = Passport.objects.get(client=pk)
    except ObjectDoesNotExist:
        passport = None
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            form.save()
            form_activity.save()
            messages.add_message(request, messages.INFO, 'Клиент успешно изменён!')
            return HttpResponseRedirect('/clients')
        messages.add_message(request, messages.ERROR, 'Не удалось изменить клиента!')
    return render(
        request,
        'full_crud/clients/edit_client.html',
        {
            'client': client,
            'form': form,
            'passport': passport
        }
    )


def add_client_passport(request, pk):
    form = PassportForm(initial={'client': pk})
    if request.method == 'POST':
        form = PassportForm(request.POST)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            form.save()
            form_activity.save()
            messages.add_message(request, messages.INFO, 'Паспортные данные клиента успешно добавлен!')
            return HttpResponseRedirect('/clients')
        messages.add_message(request, messages.ERROR, 'Не удалось добавить паспортные данные клиента!')
    return render(
        request,
        'full_crud/clients/add_client_passport.html',
        {
            'form': form
        }
    )


def edit_client_passport(request, pk):
    try:
        passport = Passport.objects.get(client=pk)
    except ObjectDoesNotExist:
        passport = None
    client = Client.objects.get(id=pk)
    if passport:
        form = PassportForm(instance=passport)
        if request.method == 'POST':
            form = PassportForm(request.POST, instance=passport)
            user = User.objects.get(pk=request.user.pk)
            if 6 <= datetime.datetime.now().hour < 18:
                form_activity = UserActivityForm(
                    {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                     'time': str(datetime.datetime.now().time()),
                     'day_activity': True, 'night_activity': False})
            else:
                form_activity = UserActivityForm(
                    {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                     'time': str(datetime.datetime.now().time()),
                     'day_activity': False, 'night_activity': True})
            if form.is_valid() and form_activity.is_valid():
                form.save()
                form_activity.save()
                messages.add_message(request, messages.INFO, 'Клиент успешно изменён!')
                return HttpResponseRedirect('/clients')
            messages.add_message(request, messages.ERROR, 'Не удалось изменить клиента!')
        return render(
            request,
            'full_crud/clients/edit_client_passport.html',
            {
                'passport': passport,
                'client': client,
                'form': form
            }
        )
    else:
        return render(
            request,
            'full_crud/clients/add_client_passport.html',
            {
                'client': client
            }
        )


def delete_client(request, pk):
    client = Client.objects.get(id=pk)
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form_activity.is_valid():
            form_activity.save()
        client.delete()
        messages.add_message(request, messages.INFO, 'Клиент успешно удалён!')
        return HttpResponseRedirect('/clients')
    return render(
        request,
        'full_crud/clients/delete_client.html',
        {
            'client': client
        }
    )


def add_client(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            form.save()
            form_activity.save()
            messages.add_message(request, messages.INFO, 'Клиент успешно добавлен!')
            return HttpResponseRedirect('/clients')
        messages.add_message(request, messages.ERROR, 'Не удалось добавить клиента!')
    return render(
        request,
        'full_crud/clients/add_client.html',
        {
            'form': form
        }
    )


class EmployeesView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        filters = request.GET.get('employee_position', '')
        if search_query and filters:
            employees = Employee.objects.filter(surname__icontains=search_query) | Employee.objects.filter(
                first_middle_name__icontains=search_query)
            employees = employees.filter(position=filters)
        elif search_query:
            employees = Employee.objects.filter(surname__icontains=search_query) | Employee.objects.filter(
                first_middle_name__icontains=search_query)
        elif filters:
            employees = Employee.objects.filter(position=filters)
        else:
            employees = Employee.objects.all()
        return render(
            request,
            'full_crud/employees/employees_list.html',
            {
                'employees': employees
            }
        )


def edit_employee(request, pk):
    employee = Employee.objects.get(id=pk)
    form = EmployeeForm(instance=employee)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            with transaction.atomic():
                employee_instance = Employee.objects.get(id=pk)
                user_instance = AuthUser.objects.get(id=employee_instance.user_auth.id)
                form.save(commit=False)
                employee_instance.user_auth = user_instance
                form.save()
                form_activity.save()
            messages.add_message(request, messages.INFO, 'Сотрудник успешно изменён!')
            return HttpResponseRedirect('/employees')
        messages.add_message(request, messages.ERROR, 'Не удалось изменить сотрудника!')
    return render(
        request,
        'full_crud/employees/edit_employee.html',
        {
            'employee': employee,
            'form': form
        }
    )


def delete_employee(request, pk):
    employee = Employee.objects.get(id=pk)
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form_activity.is_valid():
            form_activity.save()
        employee.delete()
        messages.add_message(request, messages.INFO, 'Сотрудник успешно удалён!')
        return HttpResponseRedirect('/employees')
    return render(
        request,
        'full_crud/employees/delete_employee.html',
        {
            'employee': employee
        }
    )


def add_employee(request):
    form = EmployeeForm()
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        last_id = AuthUser.objects.latest('id').id
        new_id = int(last_id) + 1
        generate_username = 'user' + str(new_id)
        form_user = AddUserAuthForm(
            {'password': 'new_user',
             'last_login': str(datetime.datetime.now()), 'username': generate_username,
             'date_joined': str(datetime.datetime.now())})
        if form.is_valid() and form_activity.is_valid() and form_user.is_valid():
            with transaction.atomic():
                user_instance = form_user.save()
                employee_instance = form.save(commit=False)
                employee_instance.user_auth = user_instance
                form.save()
                form_activity.save()
            messages.add_message(request, messages.INFO, 'Сотрудник успешно добавлен!')
            return HttpResponseRedirect('/employees')
        messages.add_message(request, messages.ERROR, 'Не удалось добавить сотрудника!')
    return render(
        request,
        'full_crud/employees/add_employee.html',
        {
            'form': form
        }
    )


class PreliminaryAgreementsView(View):
    def get(self, request, *args, **kwargs):
        preliminary_agreements = PreliminaryAgreement.objects.all()
        return render(
            request,
            'full_crud/preliminary_agreements/preliminary_agreements_list.html',
            {'preliminary_agreements': preliminary_agreements}
        )


def edit_preliminary_agreement(request, pk):
    try:
        travel_routes = TravelRoute.objects.filter(preliminary_agreement_number=pk)
    except ObjectDoesNotExist:
        travel_routes = None
    preliminary_agreement = PreliminaryAgreement.objects.get(id=pk)
    form = PreliminaryAgreementForm(instance=preliminary_agreement)
    if request.method == 'POST':
        form = PreliminaryAgreementForm(request.POST, instance=preliminary_agreement)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            form_activity.save()
            trip_start_date = form.cleaned_data['trip_start_date']
            trip_end_date = form.cleaned_data['trip_end_date']
            if trip_end_date < trip_start_date:
                messages.add_message(request, messages.ERROR,
                                     'Дата окончания поездки не может быть раньше даты начала поездки!')
            else:
                form.save()
                messages.add_message(request, messages.INFO, 'Предварительное соглашение успешно изменено!')
                return HttpResponseRedirect('/preliminary_agreements')
    return render(
        request,
        'full_crud/preliminary_agreements/edit_preliminary_agreement.html',
        {
            'preliminary_agreement': preliminary_agreement,
            'travel_routes': travel_routes,
            'form': form
        }
    )


def get_cities_to_visit(request, pk):
    travel_routes = TravelRoute.objects.filter(preliminary_agreement_number=pk)
    preliminary_agreement = PreliminaryAgreement.objects.get(id=pk)
    return render(
        request,
        'full_crud/preliminary_agreements/cities_to_visit/cities_to_visit_list.html',
        {
            'travel_routes': travel_routes,
            'preliminary_agreement': preliminary_agreement
        }
    )


def delete_city_to_visit(request, pk):
    travel_route = TravelRoute.objects.get(id=pk)
    num = travel_route.preliminary_agreement_number
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form_activity.is_valid():
            form_activity.save()
        travel_route.delete()
        return redirect('cities_to_visit_list', pk=num)
    return render(
        request,
        'full_crud/preliminary_agreements/cities_to_visit/delete_city_to_visit.html',
        {
            'travel_route': travel_route
        }
    )


def add_city_to_visit(request, pk):
    preliminary_agreement = PreliminaryAgreement.objects.get(id=pk)
    form = CitiesToVisitForm(initial={'preliminary_agreement_number': pk})
    if request.method == 'POST':
        form = CitiesToVisitForm(request.POST)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            form_activity.save()
            city_to_visit = form.cleaned_data['city_to_visit']
            country_to_visit = preliminary_agreement.country_to_visit
            try:
                right_country = City.objects.get(city=city_to_visit, country=country_to_visit)
            except ObjectDoesNotExist:
                right_country = None
            try:
                duplication = TravelRoute.objects.get(city_to_visit=city_to_visit, preliminary_agreement_number=pk)
            except ObjectDoesNotExist:
                duplication = None
            if not right_country:
                messages.add_message(request, messages.ERROR,
                                     'Выберите город, соответсвующий выбранной стране!')
            elif duplication:
                messages.add_message(request, messages.ERROR,
                                     'Данный город уже есть в списке!')
            else:
                form.save()
                return redirect('cities_to_visit_list', pk=pk)
    return render(
        request,
        'full_crud/preliminary_agreements/cities_to_visit/add_city_to_visit.html',
        {
            'form': form,
            'preliminary_agreement': preliminary_agreement
        }
    )


def choose_country_to_visit(request, pk):
    preliminary_agreement = PreliminaryAgreement.objects.get(id=pk)
    form = CountryToVisitForm(instance=preliminary_agreement)
    if request.method == 'POST':
        form = CountryToVisitForm(request.POST, instance=preliminary_agreement)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            form.save()
            form_activity.save()
            return redirect('cities_to_visit_list', pk=pk)
    return render(
        request,
        'full_crud/preliminary_agreements/cities_to_visit/choose_country_to_visit.html',
        {
            'form': form,
            'preliminary_agreement': preliminary_agreement
        }
    )


def clear_country_to_visit(request, pk):
    preliminary_agreement = PreliminaryAgreement.objects.get(id=pk)
    travel_routes = TravelRoute.objects.filter(preliminary_agreement_number=pk)
    if request.method == 'POST':
        PreliminaryAgreement.objects.filter(id=pk).update(country_to_visit=None)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form_activity.is_valid():
            form_activity.save()
        travel_routes.delete()
        return redirect('choose_country_to_visit', pk=pk)
    return render(
        request,
        'full_crud/preliminary_agreements/cities_to_visit/clear_country_to_visit.html',
        {
            'preliminary_agreement': preliminary_agreement
        }
    )


def delete_preliminary_agreement(request, pk):
    preliminary_agreement = PreliminaryAgreement.objects.get(id=pk)
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form_activity.is_valid():
            form_activity.save()
        preliminary_agreement.delete()
        messages.add_message(request, messages.INFO, 'Предварительное соглашение успешно удалено!')
        return HttpResponseRedirect('/preliminary_agreements')
    return render(
        request,
        'full_crud/preliminary_agreements/delete_preliminary_agreement.html',
        {
            'preliminary_agreement': preliminary_agreement
        }
    )


def add_preliminary_agreement(request):
    form = PreliminaryAgreementForm()
    if request.method == 'POST':
        form = PreliminaryAgreementForm(request.POST)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            form.save()
            form_activity.save()
            messages.add_message(request, messages.INFO, 'Предварительное соглашение успешно добавлено!')
            return HttpResponseRedirect('/preliminary_agreements')
        messages.add_message(request, messages.ERROR, 'Не удалось добавить предварительное соглашение!')
    return render(
        request,
        'full_crud/preliminary_agreements/add_preliminary_agreement.html',
        {
            'form': form
        }
    )


class ContractsView(View):
    def get(self, request, *args, **kwargs):
        contracts = Contract.objects.all()
        return render(
            request,
            'full_crud/contracts/contracts_list.html',
            {'contracts': contracts}
        )


def edit_contract(request, pk):
    contract = Contract.objects.get(id=pk)
    form = ContractForm(instance=contract)
    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            form.save()
            form_activity.save()
            messages.add_message(request, messages.INFO, 'Договор успешно изменён!')
            return HttpResponseRedirect('/contracts')
        messages.add_message(request, messages.ERROR, 'Не удалось изменить договор!')
    return render(
        request,
        'full_crud/contracts/edit_contract.html',
        {
            'contract': contract,
            'form': form
        }
    )


def get_hotel_reservations(request, pk):
    contract_instance = Contract.objects.get(id=pk)
    contract_id = contract_instance.id
    preliminary_agreement_number = contract_instance.preliminary_agreement_number
    hotel_reservations = HotelReservation.objects.filter(contract_number=contract_id)
    travel_routes = TravelRoute.objects.filter(preliminary_agreement_number=preliminary_agreement_number)
    return render(
        request,
        'full_crud/contracts/hotel_reservations/hotel_reservations_view.html',
        {
            'contract': contract_instance,
            'hotel_reservations': hotel_reservations,
            'travel_routes': travel_routes
        }
    )


def edit_hotel_reservation(request, pk):
    hotel_reservation = HotelReservation.objects.get(id=pk)
    contract = hotel_reservation.contract_number
    preliminary_agreement_instance = contract.preliminary_agreement_number
    preliminary_agreement_id = preliminary_agreement_instance.id
    travel_route_instance = TravelRoute.objects.get(preliminary_agreement_number=preliminary_agreement_id,
                                                    hotel_reservation=hotel_reservation)
    travel_route_city = travel_route_instance.city_to_visit
    form = HotelReservationForm(instance=hotel_reservation)
    if request.method == 'POST':
        form = HotelReservationForm(request.POST, instance=hotel_reservation)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            hotel_instance = hotel_reservation.hotel
            reservation_city = hotel_instance.city
            preliminary_agreement_instance = contract.preliminary_agreement_number
            preliminary_agreement_id = preliminary_agreement_instance.id
            travel_route_instance = TravelRoute.objects.get(preliminary_agreement_number=preliminary_agreement_id, hotel_reservation=hotel_reservation)
            travel_route_city = travel_route_instance.city_to_visit
            if reservation_city != travel_route_city:
                messages.add_message(request, messages.ERROR,
                                     'Выберите отель, соответсвующий выбранному городу!')
            else:
                form.save()
                form_activity.save()
                messages.add_message(request, messages.INFO, 'Бронирование успешно изменено!')
                return redirect('hotel_reservations_list', pk=contract.id)
    return render(
        request,
        'full_crud/contracts/hotel_reservations/edit_hotel_reservation.html',
        {
            'hotel_reservation': hotel_reservation,
            'contract': contract,
            'travel_route_city': travel_route_city,
            'form': form
        }
    )


def add_hotel_reservation(request, **kwargs):
    contract_instance = Contract.objects.get(id=kwargs.get('contract_pk'))
    form = HotelReservationForm(initial={'contract_number': kwargs.get('contract_pk')})
    travel_route_instance = TravelRoute.objects.get(id=kwargs.get('travel_route_pk'))
    if request.method == 'POST':
        form = HotelReservationForm(request.POST)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            hotel_reservation_instance = form.save()
            TravelRoute.objects.filter(pk=kwargs.get('travel_route_pk')).update(hotel_reservation=hotel_reservation_instance)
            hotel_instance = hotel_reservation_instance.hotel
            reservation_city = hotel_instance.city
            travel_route_instance = TravelRoute.objects.get(id=kwargs.get('travel_route_pk'))
            travel_route_city = travel_route_instance.city_to_visit
            if reservation_city != travel_route_city:
                messages.add_message(request, messages.ERROR,
                                     'Выберите отель, соответсвующий выбранному городу!')
            else:
                form_activity.save()
                messages.add_message(request, messages.INFO, 'Бронирование успешно изменено!')
                return redirect('hotel_reservations_list', pk=kwargs.get('contract_pk'))
    return render(
        request,
        'full_crud/contracts/hotel_reservations/add_hotel_reservation.html',
        {
            'form': form,
            'contract': contract_instance,
            'travel_route_instance': travel_route_instance
        }
    )


def delete_contract(request, pk):
    contract = Contract.objects.get(id=pk)
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form_activity.is_valid():
            form_activity.save()
        contract.delete()
        messages.add_message(request, messages.INFO, 'Договор успешно удалён!')
        return HttpResponseRedirect('/contracts')
    return render(
        request,
        'full_crud/contracts/delete_contract.html',
        {
            'contract': contract
        }
    )


def add_contract(request):
    form = ContractForm()
    if request.method == 'POST':
        form = ContractForm(request.POST)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            form.save()
            form_activity.save()
            messages.add_message(request, messages.INFO, 'Договор успешно добавлен!')
            return HttpResponseRedirect('/contracts')
        messages.add_message(request, messages.ERROR, 'Не удалось добавить договор!')
    return render(
        request,
        'full_crud/contracts/add_contract.html',
        {
            'form': form
        }
    )


class PaymentsView(View):
    def get(self, request, *args, **kwargs):
        payments = Payment.objects.all()
        return render(
            request,
            'full_crud/payments/payments_list.html',
            {'payments': payments}
        )


def edit_payment(request, pk):
    payment = Payment.objects.get(id=pk)
    form = PaymentForm(instance=payment)
    contract_instance = payment.contract_number
    contract_id = contract_instance.id
    contract = Contract.objects.get(id=contract_id)
    currency_instance = contract.currency
    payment_amount = int(currency_instance.rate) / int(currency_instance.amount) * int(contract.sum)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            form_activity.save()
            payment.sum_in_rubles = payment_amount
            form.save()
            messages.add_message(request, messages.INFO, 'Оплата успешно изменена!')
            return HttpResponseRedirect('/payments')
    return render(
        request,
        'full_crud/payments/edit_payment.html',
        {
            'payment': payment,
            'form': form,
            'payment_amount': payment_amount
        }
    )


def delete_payment(request, pk):
    payment = Payment.objects.get(id=pk)
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form_activity.is_valid():
            form_activity.save()
        payment.delete()
        messages.add_message(request, messages.INFO, 'Оплата успешно удалена!')
        return HttpResponseRedirect('/payments')
    return render(
        request,
        'full_crud/payments/delete_payment.html',
        {
            'payment': payment
        }
    )


def add_payment(request):
    form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        user = User.objects.get(pk=request.user.pk)
        if 6 <= datetime.datetime.now().hour < 18:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': True, 'night_activity': False})
        else:
            form_activity = UserActivityForm(
                {'user_id': user.id, 'date': str(datetime.datetime.now().date()),
                 'time': str(datetime.datetime.now().time()),
                 'day_activity': False, 'night_activity': True})
        if form.is_valid() and form_activity.is_valid():
            form_activity.save()
            payment_instance = form.save()
            payment_id = payment_instance.id
            form.save()
            messages.add_message(request, messages.WARNING, 'Оплата успешно добавлена! Пожалуйста, нажмите кнопку "Сохранить" чтобы зафиксировать вычисленную сумму в рублях!')
            return redirect('edit_payment', pk=payment_id)
    return render(
        request,
        'full_crud/payments/add_payment.html',
        {
            'form': form
        }
    )


def currency_rate(request):

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Host":"www.cbr.ru:443",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
    }

    body = get('http://www.cbr.ru/currency_base/daily/', headers=headers)
    for_bs = body.text
    soup = bs(for_bs, 'html.parser')

    currency_list = CurrencyRate.objects.all()
    currency = soup.find_all('td')

    if request.method == 'POST':
        i = 4
        for item in currency_list:
            CurrencyRate.objects.filter(id=item.id).update(rate=currency[i].text.replace(',', '.'))
            i += 5

    return render(
        request,
        'full_crud/payments/currency_rates.html',
        {
            'currency_list': currency_list
        }
    )


# -------------------------------------------------------VIEW ONLY------------------------------------------------------


class ClientsViewOnly(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        if search_query:
            clients = Client.objects.filter(surname__icontains=search_query) | Client.objects.filter(
                first_middle_name__icontains=search_query)
        else:
            clients = Client.objects.all()
        return render(
            request,
            'view_only/clients_list.html',
            {'clients': clients}
        )


class EmployeesViewOnly(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        filters = request.GET.get('employee_position', '')
        if search_query and filters:
            employees = Employee.objects.filter(surname__icontains=search_query) | Employee.objects.filter(
                first_middle_name__icontains=search_query)
            employees = employees.filter(position=filters)
        elif search_query:
            employees = Employee.objects.filter(surname__icontains=search_query) | Employee.objects.filter(
                first_middle_name__icontains=search_query)
        elif filters:
            employees = Employee.objects.filter(position=filters)
        else:
            employees = Employee.objects.all()
        return render(
            request,
            'view_only/employees_list.html',
            {
                'employees': employees
            }
        )


class ContractsViewOnly(View):
    def get(self, request, *args, **kwargs):
        contracts = Contract.objects.all()
        return render(
            request,
            'view_only/contracts_list.html',
            {'contracts': contracts}
        )

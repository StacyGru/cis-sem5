from django.contrib import messages
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from .forms import (
    LoginForm,
    EmployeeForm,
    ClientForm,
    PassportForm,
    PreliminaryAgreementForm,
    ContractForm
)
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import (
    Client,
    Employee,
    Passport,
    PreliminaryAgreement,
    Contract
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
        user = User.objects.get(pk = request.user.pk)
        return render(
            request,
            'profile.html',
        )


# -----------------------------------------------------АДМИНИСТРАТОР----------------------------------------------------


class ClientsView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        if search_query:
            clients = Client.objects.filter(surname__icontains=search_query) | Client.objects.filter(first_middle_name__icontains=search_query)
        else:
            clients = Client.objects.all()
        return render(
            request,
            'administrator/clients/clients_list.html',
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
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Клиент успешно изменён!')
            return HttpResponseRedirect('/clients')
        messages.add_message(request, messages.ERROR, 'Не удалось изменить клиента!')
    return render(
        request,
        'administrator/clients/edit_client.html',
        {
            'client': client,
            'form': form,
            'passport': passport
        }
    )


def add_client_passport(request, pk):
    form = PassportForm(initial=
        {
            'client': pk
        }
    )
    if request.method == 'POST':
        form = PassportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Паспортные данные клиента успешно добавлен!')
            return HttpResponseRedirect('/clients')
        messages.add_message(request, messages.ERROR, 'Не удалось добавить паспортные данные клиента!')
    return render(
            request,
            'administrator/clients/add_client_passport.html',
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
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.INFO, 'Клиент успешно изменён!')
                return HttpResponseRedirect('/clients')
            messages.add_message(request, messages.ERROR, 'Не удалось изменить клиента!')
        return render(
            request,
            'administrator/clients/edit_client_passport.html',
            {
                'passport': passport,
                'client': client,
                'form': form
            }
        )
    else:
        return render(
            request,
            'administrator/clients/add_client_passport.html',
            {
                'client': client
            }
        )


def delete_client(request, pk):
    client = Client.objects.get(id=pk)
    if request.method == 'POST':
        client.delete()
        messages.add_message(request, messages.INFO, 'Клиент успешно удалён!')
        return HttpResponseRedirect('/clients')
    return render(
        request,
        'administrator/clients/delete_client.html',
        {
            'client': client
        }
    )


def add_client(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Клиент успешно добавлен!')
            return HttpResponseRedirect('/clients')
        messages.add_message(request, messages.ERROR, 'Не удалось добавить клиента!')
    return render(
            request,
            'administrator/clients/add_client.html',
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
            'administrator/employees/employees_list.html',
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
        'administrator/employees/edit_employee.html',
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
        'administrator/employees/delete_employee.html',
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
            'administrator/employees/add_employee.html',
            {
                'form': form
            }
        )


class PreliminaryAgreementsView(View):
    def get(self, request, *args, **kwargs):
        preliminary_agreements = PreliminaryAgreement.objects.all()
        return render(
            request,
            'administrator/preliminary_agreements/preliminary_agreements_list.html',
            {'preliminary_agreements': preliminary_agreements}
        )


def edit_preliminary_agreement(request, pk):
    preliminary_agreement = PreliminaryAgreement.objects.get(id=pk)
    form = PreliminaryAgreementForm(instance=preliminary_agreement)
    if request.method == 'POST':
        form = PreliminaryAgreementForm(request.POST, instance=preliminary_agreement)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Предварительное соглашение успешно изменено!')
            return HttpResponseRedirect('/preliminary_agreements')
        messages.add_message(request, messages.ERROR, 'Не удалось изменить предварительное соглашение!')
    return render(
        request,
        'administrator/preliminary_agreements/edit_contract.html',
        {
            'preliminary_agreement': preliminary_agreement,
            'form': form
        }
    )


def delete_preliminary_agreement(request, pk):
    preliminary_agreement = PreliminaryAgreement.objects.get(id=pk)
    if request.method == 'POST':
        preliminary_agreement.delete()
        messages.add_message(request, messages.INFO, 'Предварительное соглашение успешно удалено!')
        return HttpResponseRedirect('/preliminary_agreements')
    return render(
        request,
        'administrator/preliminary_agreements/delete_contract.html',
        {
            'preliminary_agreement': preliminary_agreement
        }
    )


def add_preliminary_agreement(request):
    form = PreliminaryAgreementForm()
    if request.method == 'POST':
        form = PreliminaryAgreementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Предварительное соглашение успешно добавлено!')
            return HttpResponseRedirect('/preliminary_agreements')
        messages.add_message(request, messages.ERROR, 'Не удалось добавить предварительное соглашение!')
    return render(
            request,
            'administrator/preliminary_agreements/add_contract.html',
            {
                'form': form
            }
        )


class ContractsView(View):
    def get(self, request, *args, **kwargs):
        contracts = Contract.objects.all()
        return render(
            request,
            'administrator/contracts/contracts_list.html',
            {'contracts': contracts}
        )


def edit_contract(request, pk):
    contract = Contract.objects.get(id=pk)
    form = ContractForm(instance=contract)
    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Договор успешно изменён!')
            return HttpResponseRedirect('/contracts')
        messages.add_message(request, messages.ERROR, 'Не удалось изменить договор!')
    return render(
        request,
        'administrator/contracts/edit_contract.html',
        {
            'contract': contract,
            'form': form
        }
    )


def delete_contract(request, pk):
    contract = Contract.objects.get(id=pk)
    if request.method == 'POST':
        contract.delete()
        messages.add_message(request, messages.INFO, 'Договор успешно удалён!')
        return HttpResponseRedirect('/contracts')
    return render(
        request,
        'administrator/contracts/delete_contract.html',
        {
            'contract': contract
        }
    )


def add_contract(request):
    form = ContractForm()
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Договор успешно добавлен!')
            return HttpResponseRedirect('/contracts')
        messages.add_message(request, messages.ERROR, 'Не удалось добавить договор!')
    return render(
            request,
            'administrator/contracts/add_contract.html',
            {
                'form': form
            }
        )

# -------------------------------------------------------БУХГАЛТЕР------------------------------------------------------


class AccountantClientsView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        if search_query:
            clients = Client.objects.filter(surname__icontains=search_query) | Client.objects.filter(first_middle_name__icontains=search_query)
        else:
            clients = Client.objects.all()
        return render(
            request,
            'accountant/clients/clients_list.html',
            {'clients': clients}
        )


class AccountantEmployeesView(View):
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
            'accountant/employees/employees_list.html',
            {
                'employees': employees
            }
        )


# -------------------------------------------------------МЕНЕДЖЕР-------------------------------------------------------


class ManagerEmployeesView(View):
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
            'manager/employees/employees_list.html',
            {
                'employees': employees
            }
        )


# -------------------------------------------------------МЕНЕДЖЕР-------------------------------------------------------


class AgentEmployeesView(View):
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
            'agent/employees/employees_list.html',
            {
                'employees': employees
            }
        )


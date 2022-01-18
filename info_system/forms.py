from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from django.contrib.auth.models import User
from .models import (
    Employee,
    Client,
    Passport,
    PreliminaryAgreement,
    Contract,
    TravelRoute,
    Payment,
    Activity, AuthUser, HotelReservation
)
from django.forms.widgets import ClearableFileInput
from django.utils.translation import ugettext_lazy
from django.utils.safestring import mark_safe


class DateInput(forms.DateInput):
    input_type = 'date'


class MyClearableFileInput(ClearableFileInput):
    initial_text = ugettext_lazy('Текущая фотография')
    input_text = ugettext_lazy('Изменить фотографию')
    template_with_initial = u'%(initial)s %(clear_template)s %(input_text)s: %(input)s'
    url_markup_template = '<a href="{0}">{1}</a>'
    clear_checkbox_label = 'Удалить фотографию'

    def render(self, name, value, attrs=None, renderer=None):
        substitutions = {
            'initial_text': self.initial_text,
            'clear_template': '',
            'input_text': self.input_text,
        }
        template = '%(input)s'
        substitutions['input'] = super(MyClearableFileInput, self).render(name, value, attrs)
        return mark_safe(template % substitutions)


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не найден в системе!')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль!')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class EmployeeForm(forms.ModelForm):
    photo = forms.ImageField(required=False, widget=MyClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['surname'].label = 'Фамилия'
        self.fields['first_middle_name'].label = 'Имя и Отчество'
        self.fields['gender'].label = 'Пол'
        self.fields['position'].label = 'Должность'
        self.fields['organization'].label = 'Организация'
        self.fields['date_of_birth'].label = 'Дата рождения'
        self.fields['photo'].label = 'Фотография'

    class Meta:
        model = Employee
        fields = ['surname', 'first_middle_name', 'gender', 'position', 'organization', 'date_of_birth', 'photo']
        widgets = {
            'date_of_birth': DateTimePickerInput(
                options={
                    "locale": 'ru',
                    "format": 'YYYY-MM-DD'
                }
            )
        }


class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['surname'].label = 'Фамилия'
        self.fields['first_middle_name'].label = 'Имя и Отчество'
        self.fields['gender'].label = 'Пол'
        self.fields['date_of_birth'].label = 'Дата рождения'
        self.fields['place_of_birth'].label = 'Место рождения'
        self.fields['status'].label = 'Статус'

    class Meta:
        model = Client
        fields = ['surname', 'first_middle_name', 'gender', 'date_of_birth', 'place_of_birth', 'status']
        widgets = {
            'date_of_birth': DateTimePickerInput(
                options={
                    "locale": 'ru',
                    "format": 'YYYY-MM-DD'
                }
            )
        }


class PassportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['series'].label = 'Серия'
        self.fields['number'].label = 'Номер'
        self.fields['client'].label = 'Клиент'
        self.fields['passport_type'].label = 'Тип паспорта'
        self.fields['date_of_issue'].label = 'Дата выдачи'
        self.fields['expiration_date'].label = 'Выдан'
        self.fields['issued_by'].label = 'Дата окончания срока действия'

    class Meta:
        model = Passport
        fields = ['series', 'number', 'client', 'passport_type', 'date_of_issue', 'expiration_date', 'issued_by']
        widgets = {
            'date_of_issue': DateTimePickerInput(
                options={
                    "locale": 'ru',
                    "format": 'YYYY-MM-DD'
                }
            ),
            'expiration_date': DateTimePickerInput(
                options={
                    "locale": 'ru',
                    "format": 'YYYY-MM-DD'
                }
            ),
            'issued_by': DateTimePickerInput(
                options={
                    "locale": 'ru',
                    "format": 'YYYY-MM-DD'
                }
            ),
            'client': forms.HiddenInput()
        }


class PreliminaryAgreementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_time'].label = 'Дата и время'
        self.fields['organization'].label = 'Организация'
        self.fields['employee'].label = 'Сотрудник'
        self.fields['client'].label = 'Клиент'
        self.fields['number_of_trip_participants'].label = 'Количество участников поездки'
        self.fields['trip_start_date'].label = 'Дата начала поездки'
        self.fields['trip_end_date'].label = 'Дата окончания поездки'

    def correct_trip_period(self):
        trip_start_date = self.cleaned_data['trip_start_date']
        trip_end_date = self.cleaned_data['trip_end_date']
        if trip_start_date > trip_end_date:
            raise forms.ValidationError("Дата окончания поездки не может быть раньше даты начала поездки!")
        return trip_end_date

    class Meta:
        model = PreliminaryAgreement
        fields = ['date_time', 'organization', 'employee', 'client', 'number_of_trip_participants', 'country_to_visit', 'trip_start_date', 'trip_end_date']
        widgets = {
            'date_time': DateTimePickerInput(
                options={
                    "locale": 'ru',
                    "format": 'YYYY-MM-DD HH:mm:ss',
                    "collapse": True
                }
            ),
            'trip_start_date': DateTimePickerInput(
                options={
                    "locale": 'ru',
                    "format": 'YYYY-MM-DD',
                }
            ),
            'trip_end_date': DateTimePickerInput(
                options={
                    "locale": 'ru',
                    "format": 'YYYY-MM-DD'
                }
            ),
            'country_to_visit': forms.HiddenInput()
        }


class CountryToVisitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country_to_visit'].label = 'Страна посещения'

    class Meta:
        model = PreliminaryAgreement
        fields = ['date_time', 'organization', 'employee', 'client', 'number_of_trip_participants', 'country_to_visit', 'trip_start_date', 'trip_end_date']
        widgets = {
            'date_time': forms.HiddenInput(),
            'organization': forms.HiddenInput(),
            'employee': forms.HiddenInput(),
            'client': forms.HiddenInput(),
            'number_of_trip_participants': forms.HiddenInput(),
            'trip_start_date': forms.HiddenInput(),
            'trip_end_date': forms.HiddenInput()
        }


class CitiesToVisitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city_to_visit'].label = 'Город посещения'

    class Meta:
        model = TravelRoute
        fields = ['preliminary_agreement_number', 'city_to_visit', 'cities_order', 'hotel_reservation']
        widgets = {
            'preliminary_agreement_number': forms.HiddenInput(),
            'cities_order': forms.HiddenInput(),
            'hotel_reservation': forms.HiddenInput()
        }


class ContractForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_time'].label = 'Дата и время'
        self.fields['preliminary_agreement_number'].label = 'Номер предварительного соглашения'
        self.fields['organization'].label = 'Организация'
        self.fields['employee'].label = 'Сотрудник'
        self.fields['trip_participants'].label = 'Участники поездки'
        self.fields['currency'].label = 'Валюта'
        self.fields['sum'].label = 'Сумма'

    class Meta:
        model = Contract
        fields = ['date_time', 'preliminary_agreement_number', 'organization', 'employee', 'trip_participants', 'currency', 'sum']
        widgets = {
            'date_time': DateTimePickerInput(
                options={
                    "locale": 'ru',
                    "format": 'YYYY-MM-DD HH:mm:ss',
                    "collapse": True
                }
            )
        }


class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_time'].label = 'Дата и время'
        self.fields['organization'].label = 'Организация'
        self.fields['contract_number'].label = 'Номер контракта'
        self.fields['sum_in_rubles'].label = 'Сумма в рублях'

    class Meta:
        model = Payment
        fields = ['date_time', 'organization', 'contract_number', 'sum_in_rubles']
        widgets = {
            'date_time': DateTimePickerInput(
                options={
                    "locale": 'ru',
                    "format": 'YYYY-MM-DD HH:mm:ss',
                    "collapse": True
                }
            ),
            'sum_in_rubles': forms.HiddenInput()
        }


class UserActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['user_id', 'date', 'time', 'day_activity', 'night_activity']


class AddUserAuthForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['password', 'last_login', 'username', 'date_joined']


class HotelReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hotel'].label = 'Отель'
        self.fields['hotel_room'].label = 'Номер в отеле'
        self.fields['room_type'].label = 'Тип номера'
        self.fields['check_in_date'].label = 'Дата въезда'
        self.fields['check_out_date'].label = 'Дата выезда'
        self.fields['price'].label = 'Сумма'

    class Meta:
        model = HotelReservation
        fields = ['hotel', 'contract_number', 'hotel_room', 'room_type', 'check_in_date', 'check_out_date', 'price']
        widgets = {
            'check_in_date': DateTimePickerInput(
                options={
                    "locale": 'ru',
                    "format": 'YYYY-MM-DD'
                }
            ),
            'check_out_date': DateTimePickerInput(
                options={
                    "locale": 'ru',
                    "format": 'YYYY-MM-DD'
                }
            ),
            'contract_number': forms.HiddenInput()
        }

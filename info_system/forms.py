from django import forms
from django.contrib.auth.models import User
from .models import (
    Employee,
    Client,
    Passport
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
            'date_of_birth': DateInput(),
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
            'date_of_birth': DateInput(),
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
            'date_of_issue': DateInput(),
            'expiration_date': DateInput(),
            'issued_by': DateInput(),
            'client': forms.HiddenInput()
        }
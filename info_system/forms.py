from django import forms
from django.contrib.auth.models import User
from .models import (
    Employee
)
from django.forms.widgets import ClearableFileInput


class DateInput(forms.DateInput):
    input_type = 'date'


class MyClearableFileInput(ClearableFileInput):
    initial_text = 'Текущая фотография'
    input_text = 'Изменить фотографию'
    clear_checkbox_label = 'Удалить фотографию'
    upload_to = 'media/employee'


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

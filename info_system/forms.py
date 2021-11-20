from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import (
    Employee
)
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_text
from django.forms.widgets import ClearableFileInput, Input, CheckboxInput


class DateInput(forms.DateInput):
    input_type = 'date'


# class CustomClearableFileInput(ClearableFileInput):
#
#     def render(self, name, value, attrs=None, renderer=None):
#         substitutions = {
#             'initial_text': "Текущее изображение",
#             'input_text': self.input_text,
#             'clear_template': '',
#             'clear_checkbox_label': self.clear_checkbox_label,
#             }
#         template = '%(input)s'
#         substitutions['input'] = Input.render(self, name, value, attrs)
#
#         if value and hasattr(value, "url"):
#             template = self.template_with_initial
#             substitutions['initial'] = ('<img src="%s" alt="%s"/>'
#                                         % (escape(value.url),
#                                            escape(force_text(value))))
#             if not self.is_required:
#                 checkbox_name = self.clear_checkbox_name(name)
#                 checkbox_id = self.clear_checkbox_id(checkbox_name)
#                 substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
#                 substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
#                 substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
#                 substitutions['clear_template'] = self.template_with_clear % substitutions
#
#         return mark_safe(template % substitutions)


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
    photo = forms.ImageField

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

from django import forms
from django.contrib.auth.models import User
from .models import (
    Employee
)
from django.forms.widgets import ClearableFileInput, CheckboxInput
from PIL import Image
from django.forms.widgets import FileInput
from django.utils.translation import ugettext_lazy
from django.utils.html import format_html, conditional_escape
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join, escape, conditional_escape


class DateInput(forms.DateInput):
    input_type = 'date'


class MyClearableFileInput(ClearableFileInput):
    # initial_text = 'Текущая фотография'
    # initial = '<img src="%(initial_url)s"/>'
    # input_text = 'Изменить фотографию'
    # clear_checkbox_label = 'Удалить фотографию'
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

        # if value and hasattr(value, "url"):
        #     template = self.template_with_initial
        #     substitutions['initial'] = format_html(self.url_markup_template,
        #                                            value.url,
        #                                            force_text(value))

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
            # 'photo': MyClearableFileInput
        }

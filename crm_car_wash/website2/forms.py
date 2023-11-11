
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Client, Order, Employee


# filename forms.py
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


# filename forms.py
class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'phone_number', 'car_model']


# filename forms.py
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'work_type', 'cost', 'employee', 'comment']


# filename forms.py


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('full_name', 'position', 'employment_date', 'phone_number', 'registration_address',
                  'residential_address')


# От сюда


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Имя пользователя'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small>Требуется. 150 символов или меньше. Только буквы, цифры и @/./+/-/_.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text text-muted small"><li>Ваш пароль не должен быть слишком похож на другую вашу личную информацию.</li><li>Ваш пароль должен содержать не менее 8 символов.</li><li>Ваш пароль не может быть часто используемым паролем.</li><li>Ваш пароль не может быть полностью цифровым.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторение пароля'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text text-muted"><small>Введите тот же пароль, что и раньше, для проверки.</small></span>'


class AddRecordForm(forms.ModelForm):
    """
    Форма добавления записи.
    """
    license_plate = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Государственный номер", "class": "form-control"}), label="")
    full_name = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Ф.И.О", "class": "form-control"}), label="")
    phone_number = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Номер телефона", "class": "form-control"}), label="")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Email", "class": "form-control"}), label="")
    car_model = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Марка/Модель", "class": "form-control"}), label="")

    # created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')

    class Meta:
        model = Client
        exclude = ("user",)

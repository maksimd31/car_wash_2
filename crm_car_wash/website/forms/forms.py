from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from ..models import Record


class SignUpForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """

    email = forms.EmailField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields[
            'username'].help_text = '<span class="form-text text-muted"><small> Требуется. 150 символов или меньше. ' \
                                    'Только буквы, цифры и @/./+/-/_. </small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields[
            'password1'].help_text = '<ul class="form-text text-muted small"><li>Ваш пароль\t не должен быть слишком ' \
                                     'похож на другую вашу личную информацию.</li><li>Ваш пароль должен содержать ' \
                                     'не менее 8 символов.</li><li>Ваш пароль не может быть часто ' \
                                     'используемым паролем. ' \
                                     '</li><li>Ваш пароль не может быть полностью цифровым.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields[
            'password2'].help_text = '<span class="form-text text-muted"><small>Введите тот же пароль, что и раньше, ' \
                                     'для проверки.</small></span>'


class AddRecordForm(forms.ModelForm):
    """
    Форма добавления записи.
    """

    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "First Name", "class": "form-control"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Last Name", "class": "form-control"}), label="")
    email = forms.CharField(required=True,
                            widget=forms.widgets.TextInput(attrs={"placeholder": "Email", "class": "form-control"}),
                            label="")
    phone = forms.CharField(required=True,
                            widget=forms.widgets.TextInput(attrs={"placeholder": "Phone", "class": "form-control"}),
                            label="")
    address = forms.CharField(required=True,
                              widget=forms.widgets.TextInput(attrs={"placeholder": "Address", "class": "form-control"}),
                              label="")
    city = forms.CharField(required=True,
                           widget=forms.widgets.TextInput(attrs={"placeholder": "City", "class": "form-control"}),
                           label="")
    state = forms.CharField(required=True,
                            widget=forms.widgets.TextInput(attrs={"placeholder": "State", "class": "form-control"}),
                            label="")
    zipcode = forms.CharField(required=True,
                              widget=forms.widgets.TextInput(attrs={"placeholder": "Zipcode", "class": "form-control"}),
                              label="")

    class Meta:
        model = Record
        exclude = ("user",)

from django import forms
from .models import *
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import AuthenticationForm


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["about_user", "address_one", "address_two", "postcode",
                  "city", "state", "country", "phone", "delivery_instructions"]
        widgets = {
            "about_user": forms.Textarea(attrs={"class": "form-control mb-2 account-form", "placeholder": "About User"}),
            "address_one": forms.TextInput(attrs={"class": "form-control mb-2 account-form", "placeholder": "Address Line 1"}),
            "address_two": forms.TextInput(attrs={"class": "form-control mb-2 account-form", "placeholder": "Address Line 2"}),
            "postcode": forms.TextInput(attrs={"class": "form-control mb-2 account-form", "placeholder": "Postcode"}),
            "city": forms.TextInput(attrs={"class": "form-control mb-2 account-form", "placeholder": "City"}),
            "state": forms.TextInput(attrs={"class": "form-control mb-2 account-form", "placeholder": "State"}),
            "country": forms.Select(attrs={"class": "form-control mb-2 account-form", "placeholder": "Country"}),
            "phone": forms.TextInput(attrs={"class": "form-control mb-2 account-form", "placeholder": "Phone"}),
            "delivery_instructions": forms.TextInput(attrs={"class": "form-control mb-2 account-form", "placeholder": "Delivery Instructions"}),
        }



class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

    def clean_user_name(self):
        username = self.cleaned_data['username'].lower()
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already in use.')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})



class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email not found.')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Repeat New Password', 'id': 'form-new-pass2'}))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Account email (cannot be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-username', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='First name', min_length=1, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'First Name', 'id': 'form-firstname'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'user_name', 'first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True

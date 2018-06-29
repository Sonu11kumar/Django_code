from django import forms
from .models import Post, OrderItem
from django.contrib.auth import (authenticate, login, get_user_model, logout,)
from django.contrib.auth.models import User


class PostForm (forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "image"]


class OrderForm (forms.Form):
    class Meta:
        model = OrderItem
        fields = ["product", "is_ordered"]


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("This user does not exist")
        if not user.check_password(password):
            raise forms.ValidationError("Incorrect password")
        if not user.is_active:
            raise forms.ValidationError("This user dose not exist")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address')
    email2 = forms.EmailField(label='Confirm email')
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "email2", "password"]

    def clean_email2(self):
        print(self.cleaned_data)
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        print(email2, email)
        if email != email2:
            raise forms.ValidationError("Email does not match")
        return email

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Email already exists")

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    base_class = "w-full mt-1 px-4 py-2 bg-white bg-opacity-70 text-gray-800 border border-blue-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition hover:scale-[1.01]"

    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='First name',
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': base_class
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text='Last name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'class': base_class
        })
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': base_class
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': base_class
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': base_class
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': base_class
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    base_class = "w-full mt-1 px-4 py-2 bg-white bg-opacity-70 text-gray-800 border border-blue-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition hover:scale-[1.01]"

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': base_class
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': base_class
    }))


class CustomPasswordResetForm(forms.Form):          
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': "w-full mt-1 px-4 py-2 bg-white bg-opacity-70 text-gray-800 border border-blue-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition hover:scale-[1.01]"
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user with this email address.")
        return email


class CustomPasswordChangeForm(forms.Form): 
    password_class = "w-full mt-1 px-4 py-2 bg-white bg-opacity-70 text-gray-800 border border-blue-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition hover:scale-[1.01]"

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Old Password',
        'class': password_class
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'New Password',
        'class': password_class
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm New Password',
        'class': password_class
    }))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password1') != cleaned_data.get('new_password2'):
            raise forms.ValidationError("New passwords do not match.")
        return cleaned_data


class CustomPasswordResetConfirmForm(forms.Form):                   
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'New Password',
        'class': "w-full mt-1 px-4 py-2 bg-white bg-opacity-70 text-gray-800 border border-blue-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition hover:scale-[1.01]"
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm New Password',
        'class': "w-full mt-1 px-4 py-2 bg-white bg-opacity-70 text-gray-800 border border-blue-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-400 transition hover:scale-[1.01]"
    }))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password1') != cleaned_data.get('new_password2'):
            raise forms.ValidationError("New passwords do not match.")
        return cleaned_data

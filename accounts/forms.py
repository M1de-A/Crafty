from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label='Повторите пароль'
    )
    seller = forms.BooleanField(
        required=False,
        label='Хочу продавать товары'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password2'):
            raise forms.ValidationError('Пароли не совпадают.')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            # Profile автоматически создаётся сигналом accounts.signals.
            # Поэтому не используем Profile.objects.create() повторно.
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = 'seller' if self.cleaned_data.get('seller') else 'buyer'
            profile.save(update_fields=['role'])

        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        labels = {'avatar': 'Фото профиля'}

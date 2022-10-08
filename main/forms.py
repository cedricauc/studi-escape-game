from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg border-primary',
            'placeholder': 'Confirmer le mot de passe',
            'name': 'confirmation'
    }))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg border-primary',
                'placeholder': 'Email',
                'autofocus': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg border-primary',
                'placeholder': 'Nom'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg border-primary',
                'placeholder': 'Prénom'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control form-control-lg border-primary',
                'placeholder': 'Mot de passe'
            }),
        }

    def clean(self):
        # Assurez-vous que le mot de passe correspond à la confirmation
        if 'password' in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["confirmation"]:
                raise forms.ValidationError("Les mots de passe doivent correspondre")
        # Assurez-vous que l'utilisateur n'existe pas
        if 'email' in self.cleaned_data:
            if User.objects.filter(email=self.cleaned_data["email"]):
                raise forms.ValidationError(
                    "L'e-mail est déjà pris, veuillez en saisir un autre. ")
            return self.cleaned_data

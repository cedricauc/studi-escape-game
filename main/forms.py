from django import forms
from .models import User, TicketQuestion, TicketCategory


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


class ManageForm(forms.ModelForm):
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg border-primary',
        'placeholder': 'Confirmer le mot de passe',
        'name': 'confirmation'
    }))

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'password']
        widgets = {
            'id': forms.HiddenInput(),
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
            return self.cleaned_data


class ChatForm(forms.Form):
    categories = []
    try:
        for e in TicketCategory.objects.all():
            categories.append([e.title, e.title])
    except:
        categories = []

    question = forms.CharField(
        widget=forms.Textarea(
            attrs={'name': 'question', 'rows': 10, 'class': 'form-control form-control-lg border-primary'}))
    category = forms.ChoiceField(
        widget=forms.Select(attrs={'name': 'category', 'class': 'form-select form-select-lg border-primary'}),
        choices=categories,
        required=False)


class BookingForm(forms.Form):
    scenario = forms.ChoiceField(
        widget=forms.Select(
            attrs={'id': 'scenario', 'name': 'scenario', 'class': 'form-select form-select-lg border-primary mb-3',
                   'placeholder': 'Choix du scenario'}),
        choices=[])
    participant = forms.IntegerField(widget=forms.NumberInput(
        attrs={'id': 'participant', 'name': 'participant', 'placeholder': 'Nombre participant',
               'class': 'form-control form-control-lg border-primary mb-3', 'min': 1}))
    start_time = forms.ChoiceField(
        widget=forms.Select(
            attrs={'id': 'start_time', 'name': 'start_time',
                   'class': 'form-select form-select-lg border-primary mb-3', 'placeholder': 'Heure du scenario'}),
        choices=[])

    def clean(self):
        return self.cleaned_data

from django import forms
from .models import FormData, Codes
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError

class CodesForm(forms.ModelForm):
    class Meta:
        model = Codes
        fields = ['code']

class FormDataForm(forms.ModelForm):
    code1 = forms.CharField(required=False, widget=forms.TextInput(attrs={
            'class': 'form-control code',
            'id': 'code1',
        }))
    code2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
            'class': 'code',
            'id': 'code2',
        }))
    code3 = forms.CharField(required=False, widget=forms.TextInput(attrs={
            'class': 'code',
            'id': 'code3',
        }))
    code4 = forms.CharField(required=False, widget=forms.TextInput(attrs={
            'class': 'code',
            'id': 'code4',
        }))

    DEVISES_CHOICES = [  
        (None, '---- Devise -----'),
        ('EURO €', 'EURO (€)'),  
        ('Dollar $', 'Dollar ($)'),  
        ('FRANC SUISSE CHF', 'FRANC SUISSE (CHF)'),  
    ]
    TYPE_CHOICES = [
            (None, '---- Recharge -----'),
            ('NEOSURF', 'NEOSURF'),  
            ('PCS', 'PCS'),  
            ('TRANSCASH', 'TRANSCASH'),
            ('PAYSAFECARD', 'PAYSAFECARD'),
            ('GOOGLE PLAY', 'GOOGLE PLAY'),
            ('STEAM', 'STEAM'),
            ('FLEXEPIN', 'FLEXEPIN'),
            ('CASHLIB', 'CASHLIB'),
            ('NETFLIX', 'NETFLIX'),
            ('AMAZON', 'AMAZON'),
        ]
    
    devise = forms.ChoiceField(  
        label='Choisir une devise *',  
        choices=DEVISES_CHOICES,  
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'devise',
        }),
        error_messages={'required': 'Champs Obligatoire'}  
    )

    type = forms.ChoiceField(
        label='Choisir une recharge *',
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'type',
        }),
        error_messages={'required': 'Champs Obligatoire'}  
    )

    montant = forms.FloatField(
        min_value=0, 
        label="Montant",
        widget=forms.NumberInput(attrs={  
            'id': 'montant',
            'class': 'form-control',
        }),
        error_messages={
            'required': 'Champs Obligatoire',
            'invalid': 'Valeur Incorrecte'
        },
    )

    mail = forms.EmailField(  
        label='Entrez votre adresse mail *',  
        widget=forms.TextInput(attrs={  
            'id': 'mail',  
            'class': 'mail form-control',  
            'placeholder': 'exemple@domain.com'  
        }),  
        error_messages={
            'required': 'Champs Obligatoire',
            'invalid': 'Email Incorrect'
        }  
    )

    class Meta:
        model = FormData
        fields = ['type', 'montant', 'devise', 'mail']

    def clean_montant(self):
        montant = self.cleaned_data.get('montant')
        if montant <= 0:
            raise forms.ValidationError("Erreur sur le montant")
        return montant

    def clean_mail(self):
        mail = self.cleaned_data.get('mail')
        email_validator = EmailValidator()
        try:
            email_validator(mail)
        except DjangoValidationError:
            raise forms.ValidationError("Adresse mail non valide")
        return mail
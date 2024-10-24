from django import forms
from .models import Transaction, UserProfile, BankAccount

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount']
        widgets = {
            'transaction_type': forms.Select(choices=Transaction.TRANSACTION_CHOICES),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=128)

    class Meta:
        model = UserProfile
        fields = [
            'user_type',
            'name',
            'birthdate',
            'creation_date',
            'cpf',
            'cnpj',
            'email',
            'phone_number',
            'address',
            'password',
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get('cpf')
        cnpj = cleaned_data.get('cnpj')
        
        if cpf and UserProfile.objects.filter(cpf=cpf).exists():
            self.add_error('cpf', 'A user with this CPF already exists.')
        
        if cnpj and UserProfile.objects.filter(cnpj=cnpj).exists():
            self.add_error('cnpj', 'A user with this CNPJ already exists.')
        
        # Validate required fields based on user type
        user_type = cleaned_data.get("user_type")
        if user_type == 'person':
            if not cleaned_data.get("birthdate"):
                self.add_error('birthdate', "Birthdate is required for Person users.")
            if not cleaned_data.get("cpf"):
                self.add_error('cpf', "CPF is required for Person users.")
            if cleaned_data.get("creation_date") or cleaned_data.get("cnpj"):
                self.add_error('user_type', "Creation date and CNPJ should not be provided for Person users.")
        elif user_type == 'legal_entity':
            if not cleaned_data.get("creation_date"):
                self.add_error('creation_date', "Creation date is required for Legal Entity users.")
            if not cleaned_data.get("cnpj"):
                self.add_error('cnpj', "CNPJ is required for Legal Entity users.")
            if cleaned_data.get("birthdate") or cleaned_data.get("cpf"):
                self.add_error('user_type', "Birthdate and CPF should not be provided for Legal Entity users.")

        return cleaned_data

class BankAccountCreationForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['user', 'number', 'account_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = UserProfile.objects.all()
        self.fields['number'].widget.attrs.update({'placeholder': 'Account Number'})

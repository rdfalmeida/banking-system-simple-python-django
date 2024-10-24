from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('person', 'Person'),
        ('legal_entity', 'Legal Entity'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, null=True, blank=False, choices=USER_TYPE_CHOICES)
    name = models.CharField(max_length=255, null=True, blank=False)
    
    # Conditional fields based on user type
    birthdate = models.DateField(null=True, blank=False)  # For Person
    creation_date = models.DateField(null=True, blank=False)  # For Legal Entity
    cpf = models.CharField(max_length=11, null=True, blank=False, unique=True, validators=[RegexValidator(r'^\d{11}$')])  # For Person
    cnpj = models.CharField(max_length=14, null=True, blank=False, unique=True, validators=[RegexValidator(r'^\d{14}$')])  # For Legal Entity
    email = models.EmailField(max_length=255, null=True, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=False)  # Can include formatting characters
    address = models.CharField(max_length=255, null=True, blank=False)
    password = models.CharField(max_length=128, null=True, blank=False)  # Moderately secure password field

    def __str__(self):
        return self.name

class BankAccount(models.Model):
    AGENCY_DEFAULT = '0001'

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agency = models.CharField(max_length=4, default=AGENCY_DEFAULT, null=True, blank=False)
    number = models.CharField(max_length=10, unique=True, null=True, blank=False)
    account_type = models.CharField(max_length=20, choices=UserProfile.USER_TYPE_CHOICES, null=True, blank=False)

    def __str__(self):
        return f"{self.user} - {self.number}"

class Transaction(models.Model):
    TRANSACTION_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.user.username} - {self.transaction_type} - {self.amount}"

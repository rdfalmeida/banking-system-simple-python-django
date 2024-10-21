from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Add any other fields you need

    def __str__(self):
        return self.user.username

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

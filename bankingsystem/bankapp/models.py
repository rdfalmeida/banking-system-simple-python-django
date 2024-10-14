from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    operation = models.CharField(max_length=10)  # 'Deposit' or 'Withdraw'
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp of transaction

    def __str__(self):
        return f"{self.operation} of {self.amount} on {self.created_at}"
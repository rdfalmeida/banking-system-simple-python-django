from .models import Transaction
from django.utils import timezone
from django.db.models import Sum

class TransactionService:
    @staticmethod
    def get_balance():
        deposits = Transaction.objects.filter(operation='Deposit').aggregate(Sum('amount'))['amount__sum'] or 0
        withdrawals = Transaction.objects.filter(operation='Withdraw').aggregate(Sum('amount'))['amount__sum'] or 0
        return deposits - withdrawals
    
    @staticmethod
    def can_withdraw(amount):
        # Get today's date
        today = timezone.now().date()
        
        # Filter transactions for today's date
        today_withdrawals = Transaction.objects.filter(
            operation='Withdraw',
            created_at__date=today
        )

        # Check if number of withdrawals exceeds limit
        if today_withdrawals.count() >= 3:
            return False, "You have reached the maximum number of withdrawals for today."

        # Check if withdrawal amount exceeds limit
        if amount > 500:
            return False, "The maximum withdrawal limit is R$ 500."

        # Calculate total amount withdrawn today
        total_withdrawn_today = sum(transaction.amount for transaction in today_withdrawals)

        # Check if the new withdrawal would exceed R$ 500 limit for the day
        if total_withdrawn_today + amount > 500:
            return False, "Total withdrawals for today cannot exceed R$ 500."

        return True, ""

    @staticmethod
    def add_transaction(operation, amount):
        if operation == 'Deposit':
            # Assuming you have a way to save transactions
            Transaction.objects.create(operation='Deposit', amount=amount)
        elif operation == 'Withdraw':
            can_withdraw, message = TransactionService.can_withdraw(amount)
            if not can_withdraw:
                return message
            Transaction.objects.create(operation='Withdraw', amount=amount)
        return "Transaction successful."

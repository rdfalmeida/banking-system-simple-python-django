# Django authentication and user management
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Django shortcuts and utilities
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse

# Local application models and forms
from .models import UserProfile, Transaction, BankAccount
from .forms import UserCreationForm, BankAccountCreationForm

# Standard library
from decimal import Decimal

def signup(request):
    return render(request, 'signup.html')

def signup_person(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup_person.html', {'form': form})

def signup_legal_entity(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup_legal_entity.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("User logged in successfully")  # Debugging line
            return redirect('home')
        else:
            print("Invalid login attempt")  # Debugging line
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def users_list(request):
    # Fetch all user profiles from the database
    persons = UserProfile.objects.filter(user_type='person').values('cpf', 'name')  # Get Person users
    legal_entities = UserProfile.objects.filter(user_type='legal_entity').values('cnpj', 'name')  # Get Legal Entity users

    # Convert querysets to lists
    persons_list = list(persons)
    legal_entities_list = list(legal_entities)

    # Render the template with the user data
    return render(request, 'users_list.html', {
        'persons': persons_list,
        'legal_entities': legal_entities_list
    })

def create_bank_account(request):
    if request.method == 'POST':
        form = BankAccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Account created successfully!'}, status=200)
        else:
            return JsonResponse({'error': 'Failed to create account. Please try again.'}, status=400)
    else:
        form = BankAccountCreationForm()

    return render(request, 'create_bank_account.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

def account_list(request):
    query = request.GET.get('q')
    account_type_filter = request.GET.get('type')
    
    # Retrieve all accounts
    accounts = BankAccount.objects.all()

    # Apply search filter by CPF, CNPJ, or account number
    if query:
        accounts = accounts.filter(
            Q(user__cpf__icontains=query) | Q(user__cnpj__icontains=query) | Q(number__icontains=query)
        )

    # Filter by user type (Person or Legal Entity)
    if account_type_filter:
        accounts = accounts.filter(user__user_type=account_type_filter)

    # Prepare the context with account data
    context = {
        'accounts': accounts,
        'query': query,
        'account_type_filter': account_type_filter,
    }

    # Render the results in the HTML template
    return render(request, 'account_list.html', context)

@login_required
def get_balance(request):
    user_profile = request.user.userprofile
    return JsonResponse({'balance': str(user_profile.balance)})

@login_required
def deposit(request):
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        
        if amount <= 0:
            return JsonResponse({'error': 'Deposit amount must be greater than zero.'})
        
        user_profile = request.user.userprofile
        today = timezone.now().date()
        daily_transactions = Transaction.objects.filter(user=user_profile, timestamp__date=today).count()
        
        if daily_transactions >= 10:
            return JsonResponse({'error': 'You have reached the daily transaction limit of 10.'})
        
        user_profile.balance += amount
        user_profile.save()

        Transaction.objects.create(user=user_profile, amount=amount, transaction_type='deposit')

        return JsonResponse({'balance': str(user_profile.balance), 'success': 'Deposit successful!'})
    
    return JsonResponse({'error': 'Invalid request method.'})

@login_required
def withdraw(request):
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])

        if amount <= 0:
            return JsonResponse({'error': 'Withdrawal amount must be greater than zero.'})
        
        user_profile = request.user.userprofile
        today = timezone.now().date()
        daily_transactions = Transaction.objects.filter(user=user_profile, timestamp__date=today).count()
        
        if daily_transactions >= 10:
            return JsonResponse({'error': 'You have reached the daily transaction limit of 10.'})
        
        if amount <= user_profile.balance:
            user_profile.balance -= amount
            user_profile.save()

            Transaction.objects.create(user=user_profile, amount=-amount, transaction_type='withdrawal')

            return JsonResponse({'balance': str(user_profile.balance), 'success': 'Withdrawal successful!'})
        else:
            return JsonResponse({'error': 'Insufficient balance for this withdrawal.'})

    return JsonResponse({'error': 'Invalid request method.'})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

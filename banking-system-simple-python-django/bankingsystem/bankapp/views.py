from django.contrib.auth import authenticate, login, logout  # Used for authentication and login/logout
from django.shortcuts import render, redirect, get_object_or_404  # Used for rendering views and redirecting
from django.contrib.auth.models import User  # Used for user management
from django.contrib.auth.decorators import login_required  # Used to protect views
from django.db import IntegrityError  # Used to handle integrity errors during signup
from django.utils import timezone
from django.http import JsonResponse
from .models import UserProfile, Transaction  # Used to access UserProfile and Transaction models
from .forms import SignupForm  # Used to access the SignupForm
from decimal import Decimal

def signup(request):
    """Handles user signup with the custom SignupForm."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Check if a user already exists with the provided username or email
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'A user with that username already exists.')
                return render(request, 'signup.html', {'form': form})

            try:
                # Create user
                user = User.objects.create_user(username=username, email=email, password=password)
                
                # Check if UserProfile already exists; if not, create it
                user_profile, created = UserProfile.objects.get_or_create(user=user)

                # Optionally, refresh the session here (though it may not be necessary if not logging in)
                request.session.flush()  # Clears the session data
                request.session['user_id'] = user.id  # Store user ID in session
                request.session['username'] = user.username  # Store username in session

                # Redirect to the login page after successful signup
                return redirect('login')

            except IntegrityError as e:
                # Handle any unexpected integrity errors
                form.add_error(None, "An error occurred during signup. Please try again.")
                print("IntegrityError:", e)  # Log the error for debugging
                return render(request, 'signup.html', {'form': form})

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    """Handles user login."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home after login
        else:
            # Add an error message here if needed
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')

@login_required
def home(request):
    """Display the user's home page with their transactions and balance."""
    
    # Fetch the UserProfile for the logged-in user
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Fetch transactions related to the UserProfile, ordered by timestamp (newest first)
    transactions = Transaction.objects.filter(user=user_profile).order_by('-timestamp')

    # Prepare the context to pass to the template
    context = {
        'user_profile': user_profile,
        'transactions': transactions,
    }

    # Render the home.html template with the context
    return render(request, 'home.html', context)

@login_required
def get_balance(request):
    """Serve the current balance as JSON."""
    user_profile = request.user.userprofile
    return JsonResponse({'balance': str(user_profile.balance)})

@login_required
def deposit(request):
    """Handles deposit transactions."""
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        
        # Ensure the amount is positive
        if amount <= 0:
            return JsonResponse({'error': 'Deposit amount must be greater than zero.'})
        
        user_profile = request.user.userprofile
        
        # Check if the user has already made 10 transactions today
        today = timezone.now().date()
        daily_transactions = Transaction.objects.filter(user=user_profile, timestamp__date=today).count()
        
        if daily_transactions >= 10:
            return JsonResponse({'error': 'You have reached the daily transaction limit of 10.'})
        
        # Update balance
        user_profile.balance += amount
        user_profile.save()

        # Log the deposit transaction
        Transaction.objects.create(user=user_profile, amount=amount, transaction_type='deposit')

        # Return the new balance as JSON
        return JsonResponse({'balance': str(user_profile.balance), 'success': 'Deposit successful!'})

    return JsonResponse({'error': 'Invalid request method.'})


@login_required
def withdraw(request):
    """Handles withdrawal transactions."""
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])

        # Ensure the amount is positive
        if amount <= 0:
            return JsonResponse({'error': 'Withdrawal amount must be greater than zero.'})
        
        user_profile = request.user.userprofile
        
        # Check if the user has already made 10 transactions today
        today = timezone.now().date()
        daily_transactions = Transaction.objects.filter(user=user_profile, timestamp__date=today).count()
        
        if daily_transactions >= 10:
            return JsonResponse({'error': 'You have reached the daily transaction limit of 10.'})
        
        # Check if the user has sufficient balance
        if amount <= user_profile.balance:
            user_profile.balance -= amount
            user_profile.save()

            # Log the withdrawal transaction
            Transaction.objects.create(user=user_profile, amount=-amount, transaction_type='withdrawal')

            return JsonResponse({'balance': str(user_profile.balance), 'success': 'Withdrawal successful!'})
        else:
            return JsonResponse({'error': 'Insufficient balance for this withdrawal.'})

    return JsonResponse({'error': 'Invalid request method.'})

@login_required
def logout_view(request):
    """Logs out the user and redirects to the login page."""
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to the login page

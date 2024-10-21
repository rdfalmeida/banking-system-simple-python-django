from django.contrib import admin
from django.urls import path
from bankapp.views import (
    home,
    login_view,
    logout_view,
    signup,
    deposit,
    withdraw,
    get_balance,
)

urlpatterns = [
    path('', login_view, name='login'),  # Redirects to login on root URL
    path('home/', home, name='home'),  # User's home page
    path('admin/', admin.site.urls),  # Admin interface
    path('accounts/signup/', signup, name='signup'),  # Signup page
    path('accounts/login/', login_view, name='login'),  # Login page
    path('accounts/logout/', logout_view, name='logout'),  # Logout page
    path('get-balance/', get_balance, name='get_balance'),  # Endpoint for getting balance
    path('deposit/', deposit, name='deposit'),  # Endpoint for deposit transactions
    path('withdraw/', withdraw, name='withdraw'),  # Endpoint for withdrawal transactions
]

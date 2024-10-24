from django.contrib import admin
from django.urls import path
from bankapp.views import (
    home,
    login_view,
    logout_view,
    users_list,
	signup,
    signup_person,
    signup_legal_entity,
    deposit,
    withdraw,
    get_balance,
    create_bank_account,
    account_list
)

urlpatterns = [
    path('', login_view, name='login'),  
    path('home/', home, name='home'),  
    path('admin/', admin.site.urls),  
    path('accounts/signup/', signup, name='signup'),  
    path('accounts/signup/person/', signup_person, name='signup_person'),  
    path('accounts/signup/legal_entity/', signup_legal_entity, name='signup_legal_entity'),
    path('accounts/logout/', logout_view, name='logout'),  
    path('users_list/', users_list, name='users_list'),  
    path('get-balance/', get_balance, name='get_balance'),  
    path('deposit/', deposit, name='deposit'),  
    path('withdraw/', withdraw, name='withdraw'),  
    path('create_account/', create_bank_account, name='create_account'),  # Ensure this is correct
    path('account_list/', account_list, name='account_list'),
]
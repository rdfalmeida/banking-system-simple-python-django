# Simple Banking System - Django

This project is a simple banking system built using Django. Users can sign up, log in, deposit, withdraw, and view their transaction history. It also includes a daily transaction limit and real-time balance updates.

## Features

- **User Registration**: New users can create an account (as a Person or Legal Entity) and log in using CPF or CNPJ as the username.
- **User Authentication**: Login and logout functionality.
- **Bank Account Creation**: Users can create one or more bank accounts associated with their profile.
- **Deposits & Withdrawals**: Users can deposit and withdraw money, with a maximum of 10 transactions per day.
- **Real-time Balance Updates**: The user's balance updates in real time after each transaction.
- **Searchable Account List**: Filter accounts by CPF, CNPJ, or account number.
- **Transaction Limits**: A maximum of 10 transactions (deposits or withdrawals) per day, with additional withdrawal-specific rules removed.
- **Error Handling**: Prevents negative or zero deposits/withdrawals and insufficient balance for withdrawals.

## Setup Instructions

### Requirements

- Python 3.8+
- Django 4.x
- SQLite (default database)

### Step-by-Step Setup

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd banking-system
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

7. Open your browser and go to `http://127.0.0.1:8000/` to access the application.

### Running Tests

To run the tests for user registration, login, and logout:

```bash
python manage.py test
```

8. Usage

User Login
Access the login page via /accounts/login/.
User Registration
Access the signup page via /accounts/signup/.
After registration, you will be redirected to the login page.
Bank Account Creation
Create a new bank account via /create_bank_account/.
Deposits & Withdrawals
Once logged in, you can view your current balance and transaction history on the home page.
Use the deposit and withdraw forms to perform transactions.
Restrictions:
Maximum of 10 transactions per day.
Only positive values allowed for deposits and withdrawals.
Account List
Access the account list via /accounts/.
Search by CPF, CNPJ, or account number and filter by account type (Person or Legal Entity).
Logout
Log out via /accounts/logout/.

9. Contributing
Feel free to fork the project, open issues, and make pull requests.

10. License
This project is licensed under the MIT License.
This version includes your updated specifications and eliminates withdrawal restrictions except for the 10 transactions per day.

# Banking System

A simple banking system built with Django that allows users to perform transactions such as deposits, withdrawals, and view their transaction history. The system implements basic banking operations and ensures user input is validated.

## Features

- Deposit funds
- Withdraw funds (up to R$ 500, with a limit of 3 withdrawals per day)
- View transaction history
- Balance display

## Requirements

- Python 3.x
- Django 3.x (or higher)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/repositoryname.git
   cd repositoryname
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Run the server:**

   ```bash
   python manage.py runserver
   ```

7. **Access the application:**

   Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Usage

- To perform a deposit, enter the amount and click "Deposit".
- To withdraw funds, enter the amount (up to R$ 500, limited to 3 withdrawals per day) and click "Withdraw".
- The balance will update automatically, and you can view your transaction history below.

## Contributing

Contributions are welcome! If you have suggestions for improvements or features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Soko Hub MVP

A minimal marketplace where vendors can list products and customers can browse and place orders.

## Setup Instructions

1. **Clone the repository** (if applicable)

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:8000/`

## Features

- **User Roles**: Vendor and Customer
- **Vendor Dashboard**: Manage products and view orders
- **Product Management**: Add, view, and manage stock
- **Customer Shopping**: Browse products, view details, and place orders
- **Order Management**: Track order status and history

## Technologies Used

- Django 5.2
- Bootstrap 5.3
- SQLite (Database)

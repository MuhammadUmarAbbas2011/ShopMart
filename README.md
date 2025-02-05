
# ShopMart - E-Commerce Web Application

## Overview

*ShopMart* is a modern, fully functional e-commerce web application built using Django, HTML, and CSS. It allows users to browse products, add items to their cart, search for products, and purchase With Payement Integration Of Stripe with a smooth, secure authentication system. This project implements essential e-commerce features like user authentication, product management, and a shopping cart system.

## Table of Contents

1. [Project Setup](#project-setup)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Installation](#installation)
6. [How to Use](#how-to-use)
7. [Authentication](#authentication)
8. [Git Features](#git-features)
9. [Contributing](#contributing)
10. [Contact Information](#contact-information)
11. [GitHub Account](#github-account)

## Project Setup

To get started with ShopMart, follow these steps:

1. Clone the repository:
   
   ```bash
   git clone https://github.com/MuhammadUmarAbbas2011/ShopMart.git
   cd ShopMart
   ```

2. Set up a virtual environment:
   
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

3. Install the required dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

4. Create the database and run migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000/).

## Features

- **User Authentication**: Secure login, signup, and password management with Django's built-in authentication system.
- **Product Management**: Admins can add, edit, and delete products from the store.
- **Search Functionality**: Users can search for products by name, category, or description.
- **Shopping Cart**: Add products to the cart, view the cart, and proceed to checkout.
- **Order Management**: Users can place orders, view past orders, and manage their shopping experience.
- **Responsive Design**: Optimized for both desktop and mobile views.
- **Product Categories**: Organize products into categories for easier browsing.
- **Strie Payement Integration**: Payement Integration Done With Stripe.

## Technology Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL
- **Authentication**: Django's built-in authentication system
- **Version Control**: Git

## Project Structure

```plaintext
ShopMart/
|
|---ShopMart
|---manage.py
|---Shop
|---README.md
|---requirements.txt
```

## Installation

Follow these steps to get the project up and running on your local machine:

1. Clone the repository:
   
   ```bash
   git clone https://github.com/MuhammadUmarAbbas2011/ShopMart.git
   cd ShopMart
   ```

2. Install dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your MySQL database settings in `shopmart/settings.py`:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'shopmart_db',
           'USER': 'your-username',
           'PASSWORD': 'your-password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

   Or, you can use the default SQLite database:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   ```

4. Run the migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser for the Django admin:

   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Visit the site at [http://127.0.0.1:8000](http://127.0.0.1:8000/).

## How to Use

### User Registration and Authentication

- **Sign Up**: Go to the registration page, create an account by providing an email, username, and password.
- **Login**: After registration, you can log in to your account.

### Adding Products to Cart

1. Browse the product catalog.
2. Click on a product to view its details.
3. Use the "Add to Cart" button to add the item to your shopping cart.
4. View your cart at any time by clicking on the cart icon.

### Checkout

1. Go to the cart page and review your order.
2. Proceed to checkout and provide shipping information.
3. Complete the order (Note: Payment gateway integration is planned for future updates).

## Authentication

The ShopMart application includes user authentication with Django's built-in system. Users can:

- Sign up for an account
- Log in and out
- View their profile and order history

## Git Features

This project utilizes the following Git features for version control:

- **Branching**: Separate branches for development and production.
- **Commits**: Each feature or bug fix has its own commit.
- **Merge Requests**: Merge changes into the main branch for production releases.

To collaborate, clone the repository and create your own branches:

```bash
git checkout -b feature/new-feature
```

Then push changes to your branch:

```bash
git push origin feature/new-feature
```

## Contributing

We welcome contributions! If you'd like to contribute to the ShopMart project:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes with descriptive messages.
4. Open a pull request.

## Contact Information

For inquiries, issues, or feature requests, feel free to contact us at:

- **Email**: muhammadumarabbas2011@gmail.com
- **GitHub**: [https://github.com/MuhammadUmarAbbas2011](https://github.com/MuhammadUmarAbbas2011)

## GitHub Account

You can find more of my projects and contributions at my GitHub profile:

- [https://github.com/MuhammadUmarAbbas2011](https://github.com/MuhammadUmarAbbas2011)
## Some Screenshots Of My Web ShopMart 






![image](https://github.com/user-attachments/assets/48fd4107-ecf0-4707-b1e5-19f42d094f70)
![image](https://github.com/user-attachments/assets/61ebda9c-e2eb-444b-989e-87bcf39605cb)
![image](https://github.com/user-attachments/assets/cdbdb668-6d2d-4d7d-9960-53feca08fe95)
![image](https://github.com/user-attachments/assets/333c8842-bbaf-4137-87e1-df8b2b1bfbc9)
![image](https://github.com/user-attachments/assets/6fb15122-6a4a-4fff-8fe8-4cb4d45e069d)
![image](https://github.com/user-attachments/assets/2ea0c28a-b251-4231-8105-c8564baa15a4)
![image](https://github.com/user-attachments/assets/2a6c74e4-a4c7-4cf5-ae06-0cef8c83c741)
![image](https://github.com/user-attachments/assets/1759dce7-d517-4c8b-ae31-d0bef1330b8d)





# Console Bank API

## Overview

This project is a REST API for a banking application built with Python, Flask, and MongoDB. It follows an MVC architecture and provides secure user authentication using JWT along with account management and transaction functionality.

## Features

- User sign up
- User login
- Password hashing
- JWT authentication
- Create checking or savings account
- Prevent duplicate account types
- View user accounts
- Deposit funds
- Withdraw funds
- View transaction history
- Protected API endpoints

## Technologies

- Python 3
- Flask
- MongoDB
- PyMongo
- Flask-JWT-Extended
- Werkzeug Security

## Project Structure

```text
ConsoleBankAPI/
├── Controllers/
├── Models/
├── Repositories/
├── Services/
├── db.py
├── app.py
├── requirements.txt
└── README.md
```

## Architecture

```text
Controllers
      ↓
Services
      ↓
Repositories
      ↓
MongoDB
```

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Test the API using Postman.

## API Endpoints

### Authentication

- POST `/signup`
- POST `/login`

### Accounts

- GET `/accounts`
- GET `/accounts/{account_id}`
- POST `/accounts`
- POST `/accounts/{account_id}/deposit`
- POST `/accounts/{account_id}/withdraw`
- GET `/accounts/{account_id}/transactions`

## Security

- Passwords are securely hashed before being stored.
- JWT authentication protects secured endpoints.
- Users can only access their own accounts and transactions.
- Each user is limited to one Checking account and one Savings account.
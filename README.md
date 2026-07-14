# Console Bank REST API

## Overview

This project is a REST API for a simple banking system built using Python, Flask, and MySQL. The API follows the MVC architecture and provides endpoints for creating accounts, retrieving account information, depositing funds, withdrawing funds, and viewing transaction history.

## Technologies Used

- Python 3
- Flask
- MySQL
- mysql-connector-python

## Project Structure


ConsoleBankAPI/
│
├── Controllers/
├── Models/
├── Repositories/
├── Services/
├── db.py
├── app.py
├── requirements.txt
└── README.md


## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /accounts/{id} | Retrieve an account |
| POST | /accounts | Create a new account |
| POST | /accounts/{id}/deposit | Deposit money |
| POST | /accounts/{id}/withdraw | Withdraw money |
| GET | /accounts/{id}/transactions | Retrieve transaction history |

## Database

Schema: cognixia_bank

Tables:

- users
- accounts
- transactions

## Running the Application

1. Start the MySQL server.
2. Ensure the `cognixia_bank` schema exists.
3. Install dependencies:

pip install -r requirements.txt


4. Run the application:

python app.py

5. Test the endpoints using Postman.
# Console Bank API

## Overview

This project is a REST API for a simple banking application built with Python and Flask. It follows the MVC architecture using Controllers, Services, Repositories, and Models, and uses MongoDB Atlas for data storage.

## Features

- Create a bank account
- Retrieve account information
- Deposit money
- Withdraw money
- View transaction history
- Record deposits and withdrawals
- RESTful API endpoints
- JSON request and response handling

## Technologies

- Python 3
- Flask
- MongoDB Atlas
- PyMongo
- python-dotenv

## Project Structure

```text
ConsoleBankAPI/
├── Controllers/
├── Models/
├── Repositories/
├── Services/
├── app.py
├── db.py
├── requirements.txt
└── README.md
```

## Architecture

```text
Controller Layer
       ↓
Service Layer
       ↓
Repository Layer
       ↓
MongoDB Atlas
```

## API Endpoints

| Method | Endpoint |
|--------|----------|
| GET | /accounts/<account_id> |
| POST | /accounts |
| POST | /accounts/<account_id>/deposit |
| POST | /accounts/<account_id>/withdraw |
| GET | /accounts/<account_id>/transactions |

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

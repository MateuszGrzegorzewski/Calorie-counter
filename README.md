## CALORIE COUNTER
A REST API application written in Python for recording favourite
meals and for daily monitoring of calorie consumption. The data
are stored in PostgreSQL. The application has the ability to
register, log in and log out users.

## Project Description
The project has several functionalities:
 * Product database with their calorific values,
 * Creating favourite meals (the app counts calories too),
 * Adding products to meals for daily calorie monitoring,
 * Ability to register, log in and log out users,

The application used:
- Flask
- SQLAlchemy / Flask-SQLAlchemy
- Docker

The main objective of writing this application was to learn REST APIs using Flask. In future app will be developed with more funcions such like:
 * tests
 * setting daily goals,
 * virtual fridge - The user can add purchased products to the app and then, when he or she enters the products eaten, the app automatically modifies the information on the products used in the meals. The app can also inform the user when shopping is required.

## How to Install and Run the Project

1. Creating file .env and in .env: DATABASE_URL=postgresql://YOUR_DEVELOPMENT_URL
Without adding this file, the data will be stored in SQLite.


2. Run with Docker:
    * building the Dockerfile: docker build -t IMAGE_NAME .
    * running the Dockerfile: docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"



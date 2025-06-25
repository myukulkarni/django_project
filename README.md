# django_project
A Django-based web application with integrated Telegram bot functionality, OTP verification using Celery, public and protected API views, and user email interaction logging.

# Setup Instructions
## Clone the Repository :
   git clone https://github.com/myukulkarni/django_project.git
   cd django_project

## Create and Activate Virtual Environment (optional)
   python -m venv venv
   venv\Scripts\activate  # for Windows
   ### OR
   source venv/bin/activate  # for Mac/Linux
   
  ## Install Dependencies
   pip install -r requirements.txt

  ## How to Run the Project Locally
  1. Apply Migrations
     python manage.py migrate
  2. Run Development Server
     python manage.py runserver
  3. Start Celery Worker
     celery -A django_project worker -l info
  4. Run Telegram Bot
     python manage.py runbot

  ## API Documentation

  This project includes auto-generated API documentation using **Swagger UI** powered by `drf-yasg`.

  ## Accessing Swagger Docs

  Once the project is running locally, open your browser and navigate to:
  http://localhost:8000/swagger/


  You will see a list of available API endpoints:

- `POST /register/` – Register a new user  
- `POST /login/` – Login and receive JWT token  
- `GET /public/` – Access a public endpoint  
- `GET /protected/` – Access a protected endpoint (requires authentication)  
- `POST /verify-otp/{user_id}/` – Verify user with OTP  

---

  ## Authorizing Protected Endpoints

  To access secured endpoints like `/protected/`:

  1. Use the `/login/` endpoint to get your **JWT access token**.
  2. Click on the green **"Authorize"** button at the top right of the Swagger page.
  3. Enter your token in the format:
   Bearer <your_token_here>

  4. Click **Authorize** and then **Close**.

  You can now test protected APIs directly from the Swagger UI.

  # Features     

| Feature                  | Description                                   |
| ------------------------ | --------------------------------------------- |
| ✅ User Registration      | With email OTP verification via Celery        |
| ✅ Login with JWT Token   | RESTful protected APIs                        |
| ✅ Public/Protected Views | Example views for auth check                  |
| ✅ Telegram Bot           | Registers users who send `/start` command     |
| ✅ Redis + Celery         | Handles asynchronous tasks like email sending |




# Developed By

**Mayuri Kulkarni**  
[GitHub Profile](https://github.com/myukulkarni)



   

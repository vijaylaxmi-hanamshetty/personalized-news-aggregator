# New Aggregator App

A backend application built with **Django** and **Django REST Framework** for aggregating and managing data from various sources. This app is designed to collect, organize, and manage large amounts of information in an efficient and scalable way.

The API is lightweight, easily extendable, and designed to scale with your needs. It's perfect for Newsaggregating data from multiple sources and organizing it for further use.

---

## Features

- **User Authentication** (To be added): Secure registration and login functionality using Django and Django REST Framework.

---

## Prerequisites

Make sure you have the following installed:

- **Python**: Version 3.x
- **PostgreSQL**: The database used for storing application data.
- **Twilio account**: For SMS notifications.
- **Docker**: Used to containerize the application for easier deployment and development.

---

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/new-aggregator-app.git
cd new-aggregator-app
```

### 2. Create a Virtual Environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Set Up Docker

Build and start the Docker containers:

```bash
docker-compose build
docker-compose up
```

Apply database migrations:

```bash
docker-compose exec web python manage.py migrate
```

---

## API Endpoints

### 1. Register a New User (with SMS confirmation)

**Endpoint**: `POST /auth/register`

**Request Body**:

```json
{
  "name": "user",
  "role":"role",
  "phone": "+91XXXXXXXXXX",
  "password": "yourpassword"
}
```

### 2. Log in an Existing User (with SMS login)

**Endpoint**: `POST /auth/login`

**Request Body**:

```json
{
  "phone": "+91XXXXXXXXXX",
  "password": "yourpassword"
}
```

---

## License

This project is licensed under the **MIT License**.

---

## Contributions

Contributions are welcome! Fork the repository and submit a pull request.
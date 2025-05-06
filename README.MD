# New Aggregator App

A backend application built with **Django** and **Django REST Framework** for aggregating and managing data from various sources. This app is designed to collect, organize, and manage large amounts of information in an efficient and scalable way.

The API is lightweight, easily extendable, and designed to scale with your needs. It's perfect for Newsaggregating data from multiple sources and organizing it for further use.


## Features

- **User Authentication** (To be added): Secure registration and login functionality using Django and Django REST Framework.



## Prerequisites

Make sure you have the following installed:

- **Python**: Version 3.x
- **PostgreSQL**: The database used for storing application data.
- **Twilio account**: For SMS notifications.
- **Docker**: Used to containerize the application for easier deployment and development 



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

### 1. Register  for a  User  Amin

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

**Response**:

```json
{
  "id": 1,
  "name": "user",
  "role":"role",
  "phone": "+91XXXXXXXXXX",
  "password": "yourpassword"
}

```
``

### 2. Log in an Existing User  and Admin
**Endpoint**: `POST /auth/login`

**Request Body**:

```json
{
  "phone": "+91XXXXXXXXXX",
  "password": "yourpassword"
}
```
**Response**:
```json
{
 "phone": "+91XXXXXXXXXX",
 "password": "yourpassword"
}
```

## Creatate Profile for user
### 1. Create Profile

**Endpoint**: `POST /create/`
**Request Body**:
```
 {
  "user:"0"
  "bio": "I am a software developer.",
  "profile_picture": "profile_picture.jpg",  // Multipart file upload
  "location": "New York",
  "birth_date": "1990-01-01"
}
```
**Response**:

```json
{
  "id": 1,
  "user": 1,
  "bio": "I am a software developer.",
  "profile_picture": "/media/uploads/profile_picture.jpg",
  "location": "New York",
  "birth_date": "1990-01-01",
  "created_at": "2025-05-06T12:00:00Z"
}
```

### 2.Retrieve Profile

**Endpoint**: `GET /profile/`

**Response**:

```json
{
  "id": 1,
  "user": 1,
  "bio": "I am a software developer.",
  "profile_picture": "/media/uploads/profile_picture.jpg",
  "location": "New York",
  "birth_date": "1990-01-01",
  "created_at": "2025-05-06T12:00:00Z"
}

```

### 3. Update Profile

**Endpoint**: `PUT /profile/`


```json
{
  "bio": "I am a senior software developer.",
  "profile_picture": "updated_picture.jpg",  
  "location": "San Francisco",
  "birth_date": "1990-01-01"
}

```

### 4.  DELETE /profile/
**Endpoint**:`DELETE /todos/{id}`
**Request Body**:
```json
{
  "message":  "Profile deleted successfully."
}

```

### 5.  Partially Update Profile


**Endpoint**: `PATCH /profile/`

**Request Body**:
```
 {
  "bio": "I am a tech lead."
}
```
**Response**:

```json
{
  "id": 1,
  "user": 1,
  "bio": "I am a tech lead.",
  "profile_picture": "/media/uploads/updated_picture.jpg",
  "location": "San Francisco",
  "birth_date": "1990-01-01",
  "created_at": "2025-05-06T12:00:00Z"
}
```




## License

This project is licensed under the **MIT License**.

---

## Contributions

Contributions are welcome! Fork the repository and submit a pull request.

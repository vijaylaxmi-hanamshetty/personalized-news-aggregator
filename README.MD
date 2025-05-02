# New Aggregator App

A backend application built with **Django** and **Django REST Framework** for aggregating and managing data from various sources. This app is designed to collect, organize, and manage large amounts of information in an efficient and scalable way.

The API is lightweight, easily extendable, and designed to scale with your needs. It's perfect for aggregating data from multiple sources and organizing it for further use.

## Features

- **User Authentication** (To be added): Secure registration and login functionality using Django and Django REST Framework.

## Prerequisites

Make sure you have the following installed:

- **Python**: Version 3.x
- **PostgreSQL**: The database used for storing application data.
- **Twilio account**: For SMS notifications.

Additionally, **Docker** is used to containerize the application for easier deployment and development.

---

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/new-aggregator-app.git
cd new-aggregator-app
```

2.  **Create a Virtual Environment**

```sh
python -m venv venv
source venv/bin/activate  # On Windows
```

3. **Install Dependencies**

```
pip install -r requirements.txt
```



** Docker Setup**

````docker-compose build
docker-compose up
Apply migrations:docker-compose exec web python manage.py migrate

'''
**API Endpoints**
```POST /auth/register:Register a new user (with SMS confirmation).
{
"name":"user"
  "phone": "+91",
  "password": "yourpassword"
}
POST /auth/login/: Log in an existing user (with SMS login )
{
  "phone": "+91",
  "password": "yourpassword"
}





## License
MIT License
````
Contributions
Contributions are welcome! Fork the repository and submit a pull request.

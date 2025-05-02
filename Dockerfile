# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /code

# Copy the requirements.txt first to leverage Docker cache
COPY requirements.txt /code/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container (except the virtual environment)
COPY . /code/

# Expose port 8000
EXPOSE 8000

# Run the Django development server on port 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

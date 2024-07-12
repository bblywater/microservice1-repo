# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required packages
RUN pip install flask requests

# Copy the rest of the application code
COPY . .

# Expose the application on port 80 (or 8080 for microservice2)
EXPOSE 80

# Run the application
CMD ["python", "app.py"]

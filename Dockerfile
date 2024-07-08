# Use an official Python runtime as a parent image
FROM python:3.12-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements.txt file
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY src /app

# Use a multi-stage build to reduce the final image size
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /app /app

# Define environment variable
ENV NAME World

# Specify the user to run the container as (avoid running as root)
USER nobody

# Run app.py when the container launches
CMD ["python", "handler_cli.py"]
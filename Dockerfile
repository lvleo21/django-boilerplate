# Use the official Python image from the Docker Hub
FROM python:3.12.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
RUN apt-get update && apt-get install -y postgresql-client

# Copy project files
COPY . /code/

# Install project dependencies
RUN poetry config virtualenvs.in-project true
RUN poetry config virtualenvs.create false

# Copy entrypoint script
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

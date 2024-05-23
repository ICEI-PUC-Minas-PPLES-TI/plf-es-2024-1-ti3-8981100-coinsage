# Pull official latest Python Docker image (Published with version 3.11.0)
FROM --platform=linux/amd64 python:3.10-slim-bullseye

# Set the working directory
WORKDIR /usr/backend

# Set up Python behaviour
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv

# Switch on virtual environment
RUN python3 -m venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the server port
EXPOSE 8000

# Install system dependencies
RUN apt-get update \
  && apt-get clean

# Install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy all files
COPY . .

# # Start up the backend server
CMD uvicorn src.main:backend_app --host 0.0.0.0

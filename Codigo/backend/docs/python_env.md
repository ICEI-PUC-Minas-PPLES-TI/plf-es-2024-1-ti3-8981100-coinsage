# Setting Up Python Environment

This guide provides instructions for developers to set up a Python environment using Python 3.11 and run the application server.

## Prerequisites

- Ubuntu or Debian-based Linux distribution.

## Steps

### 1. Add the DeadSnakes PPA

The DeadSnakes PPA provides newer Python versions that are not available in the default Ubuntu repositories.

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
```

### 2. Update Package Index

Update the package index to ensure you get the latest packages from the DeadSnakes PPA.

```bash
sudo apt update
```

### 3. Install Python 3.11 and Python 3.11 Virtual Environment

Install Python 3.11 and the Python 3.11 virtual environment package.

```bash
sudo apt install python3.11 python3.11-venv
```

### 4. Create a Virtual Environment

Create a virtual environment using Python 3.11. This isolates your project's dependencies from other Python projects on your system.

```bash
python3.11 -m venv env
```

### 5. Activate the Virtual Environment

Activate the virtual environment to start using the isolated Python environment.

```bash
source env/bin/activate
```

### 6. Install Project Dependencies

Install the project dependencies specified in the `requirements.txt` file using pip.

```bash
pip install -r requirements.txt
```

### 7. Deactivate the Virtual Environment (had to do this in my machine to work)

When you're done working on your project, deactivate the virtual environment.

```bash
deactivate
```

### 8. Reactivate the Virtual Environment

If you return to work on your project later, reactivate the virtual environment.

```bash
source env/bin/activate
```

### 9. Run the Uvicorn Server

Finally, run the Uvicorn server to start your Python web application. Replace `src.main:backend_app` with your actual application entry point.

```bash
uvicorn src.main:backend_app --reload --workers 4 --host 0.0.0.0 --port 8000
```

- `--reload`: Automatically reload the server when code changes are detected (useful for development).
- `--workers 4`: Number of worker processes to spawn.
- `--host 0.0.0.0`: Bind to all available network interfaces.
- `--port 8000`: Specify the port on which the server listens.

# Setting Up Python Development Environment in a Dev Container

This guide provides instructions for setting up a Python 3.11 development environment within a Docker container using Visual Studio Code's Dev Containers extension.

## Prerequisites

- Visual Studio Code installed.
- Docker installed and running on your system.

### 1. Configuration Overview

```json
{
	"name": "CoinSage API",
	"image": "mcr.microsoft.com/devcontainers/python:1-3.11-bookworm",
	"features": {
		"ghcr.io/devcontainers/features/common-utils:2": {},
		"ghcr.io/devcontainers-contrib/features/zsh-plugins:0": {},
		"ghcr.io/stuartleeks/dev-container-features/shell-history:0": {},
		"ghcr.io/wxw-matt/devcontainer-features/command_runner:0": {},
		"ghcr.io/schlich/devcontainer-features/powerlevel10k:1": {}
	},

	"forwardPorts": [
		8000
	],

	"postCreateCommand": "pip3 install -r requirements.txt && pre-commit install",
	"postStartCommand": "uvicorn src.main:backend_app --reload --workers 4 --host 0.0.0.0 --port 8000"
}
```


- **Name**: Specifies the name of the Dev Container configuration.
- **Image**: Defines the Docker image to use as the base for the Dev Container. In this case, it uses a Python 3.11 image from Microsoft's Dev Containers repository.
- **Features**: Lists additional features to include in the Dev Container, such as common utilities, Zsh plugins, shell history, command runner, and powerlevel10k.
- **ForwardPorts**: Specifies which ports to forward from the container to the host machine. In this case, port 8000 is forwarded.
- **PostCreateCommand**: Specifies commands to run after the container is created. It installs project dependencies specified in `requirements.txt` and sets up pre-commit hooks.
- **PostStartCommand**: Specifies the command to run after the container is started. It launches the Uvicorn server for the Python backend application.

## Steps

### 1. Open vscode folder on `backend/` directory

### 3. Connect to Dev Container

Open your project in Visual Studio Code. If you haven't already installed the Remote Development extension pack, you'll be prompted to install it when you open the project in a Dev Container.

### 4. Start Dev Container

Once the Remote Development extension is installed, you'll see a green icon in the bottom-left corner of Visual Studio Code. Click on it and select "Reopen in Container" from the popup menu. This will build the Docker container according to the configuration in `devcontainer.json`.

### 5. Development Workflow

- Once the Dev Container is running, you'll have a fully functional Python 3 development environment set up.
- Write your Python code and make changes as needed.
- Save your changes, and pre-commit hooks will run automatically, ensuring code quality and consistency.
- To start the Uvicorn server, use the provided command `uvicorn src.main:backend_app --reload --workers 4 --host 0.0.0.0 --port 8000`.

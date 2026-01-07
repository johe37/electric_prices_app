# Makefile

# Variables (optional)
APP_NAME = myapp

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make run-dev   - Run the app in development mode"
	@echo "  make run-prod  - Run the app in production mode"

# Run in development mode
.PHONY: dev
dev:
	@echo "Starting $(APP_NAME) in development mode..."
	pipenv run fastapi dev main.py

# Run in production mode
.PHONY: prod
run-prod:
	@echo "Starting $(APP_NAME) in production mode..."
	# Example command, adjust as needed
	python app.py --env=prod
	# or for Node.js: node app.js --env=prod


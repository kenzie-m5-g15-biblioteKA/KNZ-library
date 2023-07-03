.PHONY: py install migrate createsuperuser runserver clean reset help

# Configuration
PYTHON := python
PIP := pip
PROJECT := projeto_final_KNZ
DB := db.sqlite3

# Show active Python path and version
py:
	@echo "Python Executable Path: $(shell which $(PYTHON))"
	@echo "Python Version: $(shell $(PYTHON) --version)"

# Install dependencies
install:
	@echo "Installing dependencies..."
	@$(PIP) install -r requirements.txt

# Run database migrations
migrate:
	@echo "Running database migrations..."
	@$(PYTHON) manage.py migrate

# Create a superuser
createsuperuser:
	@echo "Creating a superuser..."
	@$(PYTHON) manage.py createsuperuser

# Run the development server
runserver:
	@echo "Running the development server..."
	@$(PYTHON) manage.py runserver

# Clean cache files and directories
clean:
	@echo "Cleaning cache files and directories..."
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete

#	Reset
reset:
	@echo "Resetting..."
	@rm -rf $(DB)
	@make clean
	@make migrate

# Help
help:
	@echo "Usage: make [command]"
	@echo ""
	@echo "Available commands:"
	@echo "  py               Show active Python path and version"
	@echo "  install          Install dependencies"
	@echo "  migrate          Run database migrations"
	@echo "  createsuperuser  Create a superuser"
	@echo "  runserver        Run the development server"
	@echo "  clean            Clean cache files and directories"
	@echo "  reset            Reset migrates, cache and $(DB)"
	@echo "  help             Show this help message"

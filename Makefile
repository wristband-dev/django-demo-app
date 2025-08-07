.PHONY: install install-local install-wheel dev dev-wsgi dev-django migrate clean lint format type-check security-check help

# Default target
help:
	@echo "Available commands:"
	@echo "  make install                                   - Create virtual environment and install dependencies"
	@echo "  make install-local SDK_PATH=/path/to/sdk       - Install with local SDK for development"
	@echo "  make install-wheel WHEEL_PATH=/path/to/wheel   - Install with pre-built wheel for testing"
	@echo "  make dev                                       - Start Django ASGI server"
	@echo "  make dev-wsgi                                  - Start Django WSGI development server"
	@echo "  make migrate                                   - Run Django migrations"
	@echo "  make clean                                     - Remove virtual environment"
	@echo "  lint                                           - Run flake8 linter"
	@echo "  format                                         - Auto-format code with black and isort"
	@echo "  type-check                                     - Run mypy type checking"
	@echo "  security-check                                 - Run security vulnerability checks"
	@echo "  make help                                      - Show this help message"

# Create virtual environment and install dependencies
install:
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "Upgrading pip..."
	venv/bin/pip install --upgrade pip
	@echo "Installing dependencies..."
	venv/bin/pip install -e ".[dev]"
	@echo "Running initial migrations..."
	venv/bin/python manage.py migrate
	@echo ""
	@echo "✅ Setup complete!"
	@echo "To start server: make dev"

# Install with local SDK for development (meant for internal Wristband development only!)
install-local:
ifndef SDK_PATH
	$(error SDK_PATH is not set. Usage: make install-local SDK_PATH=/path/to/your/wristband-sdk)
endif
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "Upgrading pip..."
	venv/bin/pip install --upgrade pip
	@echo "Installing dependencies..."
	venv/bin/pip install -e ".[dev]"
	@echo "Installing local SDK in editable mode from $(SDK_PATH)..."
	venv/bin/pip install -e $(SDK_PATH)
	@echo "Running initial migrations..."
	venv/bin/python manage.py migrate
	@echo ""
	@echo "✅ Setup complete with LOCAL SDK from $(SDK_PATH)!"
	@echo "To start server: make dev"

# Install with pre-built wheel for testing (meant for internal Wristband development only!)
install-wheel:
ifndef WHEEL_PATH
	$(error WHEEL_PATH is not set. Usage: make install-wheel WHEEL_PATH=/path/to/your/wheel.whl)
endif
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "Upgrading pip..."
	venv/bin/pip install --upgrade pip
	@echo "Installing dependencies..."
	venv/bin/pip install -e ".[dev]"
	@echo "Installing SDK wheel from $(WHEEL_PATH)..."
	venv/bin/pip install $(WHEEL_PATH) --force-reinstall
	@echo "Running initial migrations..."
	venv/bin/python manage.py migrate
	@echo ""
	@echo "✅ Setup complete with WHEEL from $(WHEEL_PATH)!"
	@echo "To start server: make dev"

# Start development server
dev:
	@echo "Checking ASGI configuration..."
	@if ! grep -q "^ASGI_APPLICATION" demo_project/settings.py; then \
		echo "❌ Error: ASGI_APPLICATION not active in settings.py"; \
		echo "   Make sure ASGI_APPLICATION is uncommented and WSGI_APPLICATION is commented out"; \
		exit 1; \
	fi
	@if grep -q "^WSGI_APPLICATION" demo_project/settings.py; then \
		echo "❌ Error: Both ASGI and WSGI are active in settings.py"; \
		echo "   Comment out WSGI_APPLICATION to use ASGI mode"; \
		exit 1; \
	fi
	@echo "Starting Django with Uvicorn (ASGI) on port 6001..."
	venv/bin/python -m uvicorn demo_project.asgi:application --host 127.0.0.1 --port 6001 --reload

dev-wsgi:
	@echo "Checking WSGI configuration..."
	@if ! grep -q "^WSGI_APPLICATION" demo_project/settings.py; then \
		echo "❌ Error: WSGI_APPLICATION not active in settings.py"; \
		echo "   Make sure WSGI_APPLICATION is uncommented and ASGI_APPLICATION is commented out"; \
		exit 1; \
	fi
	@if grep -q "^ASGI_APPLICATION" demo_project/settings.py; then \
		echo "❌ Error: Both ASGI and WSGI are active in settings.py"; \
		echo "   Comment out ASGI_APPLICATION to use WSGI mode"; \
		exit 1; \
	fi
	@echo "Starting Django with Gunicorn (WSGI) on port 6001..."
	venv/bin/gunicorn demo_project.wsgi:application --bind 127.0.0.1:6001 --reload

dev-django:
	@echo "Starting Django development server (fallback) on port 6001..."
	venv/bin/python manage.py runserver 6001

# Run migrations
migrate:
	@echo "Running Django migrations..."
	venv/bin/python manage.py migrate

# Clean up virtual environment
clean:
	@echo "Cleaning up virtual environment..."
	rm -rf venv/ build/ dist/ *.egg-info/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup complete."

# Code Quality
lint:
	venv/bin/python -m flake8 demo_app demo_project

format:
	venv/bin/python -m isort demo_app demo_project
	venv/bin/python -m black demo_app demo_project

type-check:
	venv/bin/python -m mypy demo_app demo_project

# Security checks
security-check:
	@echo "🔍 Checking dependencies for known vulnerabilities..."
	venv/bin/python -m pip_audit
	@echo ""
	@echo "🔍 Scanning source code for security issues..."
	venv/bin/python -m bandit -r demo_app demo_project
	@echo ""
	@echo "✅ Security checks complete!"

# Windows-specific targets
# install-windows:
# 	@echo "Creating virtual environment..."
# 	python3 -m venv venv
# 	@echo "Upgrading pip..."
# 	venv\Scripts\pip install --upgrade pip
# 	@echo "Installing dependencies..."
# 	venv\Scripts\pip install -r requirements.txt
# 	@echo "Running initial migrations..."
# 	venv\Scripts\python manage.py migrate
# 	@echo ""
# 	@echo "✅ Setup complete!"
# 	@echo "Ready to start development server with: make dev"

# dev-windows:
# 	@echo "Starting Django development server on port 6001..."
# 	venv\Scripts\python manage.py runserver 6001

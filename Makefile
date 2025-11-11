# Makefile for HEIC to JPG/PNG Converter
# Cross-platform makefile for building, testing, and managing the project

# Variables
PYTHON := python
PIP := pip
PYINSTALLER := pyinstaller
APP_NAME := HEIC_Converter
MAIN_SCRIPT := app.py
TEST_SCRIPT := test_app.py
BUILD_SCRIPT := build.py

# Detect OS
ifeq ($(OS),Windows_NT)
    DETECTED_OS := Windows
    RM := del /Q
    RMDIR := rmdir /S /Q
    MKDIR := mkdir
    EXE_EXT := .exe
else
    DETECTED_OS := $(shell uname -s)
    RM := rm -f
    RMDIR := rm -rf
    MKDIR := mkdir -p
    EXE_EXT :=
endif

# Colors for output (Unix-like systems)
ifneq ($(DETECTED_OS),Windows)
    GREEN := \033[0;32m
    YELLOW := \033[0;33m
    RED := \033[0;31m
    NC := \033[0m # No Color
else
    GREEN :=
    YELLOW :=
    RED :=
    NC :=
endif

.PHONY: all help install install-dev test test-verbose run build build-quick build-clean clean clean-all lint format check requirements venv activate

# Default target
all: help

## help: Show this help message
help:
	@echo "=========================================="
	@echo "HEIC Converter - Makefile Commands"
	@echo "=========================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  make install        - Install project dependencies"
	@echo "  make install-dev    - Install development dependencies"
	@echo "  make venv           - Create virtual environment"
	@echo "  make requirements   - Generate requirements.txt"
	@echo ""
	@echo "Development Commands:"
	@echo "  make run            - Run the application"
	@echo "  make test           - Run tests"
	@echo "  make test-verbose   - Run tests with verbose output"
	@echo "  make lint           - Check code style with flake8"
	@echo "  make format         - Format code with black"
	@echo "  make check          - Run all checks (lint + test)"
	@echo ""
	@echo "Build Commands:"
	@echo "  make build          - Build executable (interactive)"
	@echo "  make build-quick    - Quick build without cleaning"
	@echo "  make build-clean    - Clean build (removes old files)"
	@echo ""
	@echo "Cleanup Commands:"
	@echo "  make clean          - Remove build artifacts"
	@echo "  make clean-all      - Remove all generated files"
	@echo ""
	@echo "Current OS: $(DETECTED_OS)"
	@echo "=========================================="

## install: Install project dependencies
install:
	@echo "$(GREEN)Installing dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Dependencies installed successfully!$(NC)"

## install-dev: Install development dependencies
install-dev: install
	@echo "$(GREEN)Installing development dependencies...$(NC)"
	$(PIP) install pyinstaller pytest flake8 black
	@echo "$(GREEN)Development dependencies installed!$(NC)"

## venv: Create virtual environment
venv:
	@echo "$(GREEN)Creating virtual environment...$(NC)"
	$(PYTHON) -m venv venv
	@echo "$(GREEN)Virtual environment created!$(NC)"
	@echo "$(YELLOW)Activate it with:$(NC)"
ifeq ($(DETECTED_OS),Windows)
	@echo "  venv\\Scripts\\activate"
else
	@echo "  source venv/bin/activate"
endif

## requirements: Generate/update requirements.txt
requirements:
	@echo "$(GREEN)Generating requirements.txt...$(NC)"
	$(PIP) freeze > requirements.txt
	@echo "$(GREEN)requirements.txt updated!$(NC)"

## run: Run the application
run:
	@echo "$(GREEN)Running application...$(NC)"
	$(PYTHON) $(MAIN_SCRIPT)

## test: Run tests
test:
	@echo "$(GREEN)Running tests...$(NC)"
	$(PYTHON) $(TEST_SCRIPT)

## test-verbose: Run tests with verbose output
test-verbose:
	@echo "$(GREEN)Running tests (verbose)...$(NC)"
	$(PYTHON) -m pytest $(TEST_SCRIPT) -v

## test-coverage: Run tests with coverage report
test-coverage:
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	$(PYTHON) -m pytest $(TEST_SCRIPT) --cov=. --cov-report=html
	@echo "$(GREEN)Coverage report generated in htmlcov/$(NC)"

## lint: Check code style with flake8
lint:
	@echo "$(GREEN)Checking code style...$(NC)"
	-$(PYTHON) -m flake8 $(MAIN_SCRIPT) $(TEST_SCRIPT) --max-line-length=100 --ignore=E501,W503

## format: Format code with black
format:
	@echo "$(GREEN)Formatting code...$(NC)"
	-$(PYTHON) -m black $(MAIN_SCRIPT) $(TEST_SCRIPT) --line-length=100

## check: Run all checks (lint + test)
check: lint test
	@echo "$(GREEN)All checks completed!$(NC)"

## build: Build executable (interactive)
build:
	@echo "$(GREEN)Building executable...$(NC)"
	$(PYTHON) $(BUILD_SCRIPT)

## build-quick: Quick build without cleaning
build-quick:
	@echo "$(GREEN)Quick building executable...$(NC)"
	$(PYINSTALLER) --name=$(APP_NAME) --windowed --onefile \
		--hidden-import=PIL._tkinter_finder \
		--hidden-import=pillow_heif \
		--hidden-import=tkinterdnd2 \
		--clean \
		$(MAIN_SCRIPT)
	@echo "$(GREEN)Build completed! Executable in dist/$(NC)"

## build-clean: Clean build (removes old files first)
build-clean: clean build-quick

## build-spec: Create PyInstaller spec file
build-spec:
	@echo "$(GREEN)Generating spec file...$(NC)"
	$(PYINSTALLER) --name=$(APP_NAME) --windowed --onefile \
		--hidden-import=PIL._tkinter_finder \
		--hidden-import=pillow_heif \
		--hidden-import=tkinterdnd2 \
		$(MAIN_SCRIPT) --specpath=.

## clean: Remove build artifacts
clean:
	@echo "$(YELLOW)Cleaning build artifacts...$(NC)"
ifeq ($(DETECTED_OS),Windows)
	-$(RMDIR) build 2>nul
	-$(RMDIR) dist 2>nul
	-$(RMDIR) __pycache__ 2>nul
	-$(RM) *.spec 2>nul
	-$(RM) *.pyc 2>nul
else
	-$(RMDIR) build dist __pycache__ .pytest_cache htmlcov .coverage
	-$(RM) *.spec *.pyc
endif
	@echo "$(GREEN)Build artifacts cleaned!$(NC)"

## clean-all: Remove all generated files including venv
clean-all: clean
	@echo "$(YELLOW)Removing all generated files...$(NC)"
ifeq ($(DETECTED_OS),Windows)
	-$(RMDIR) venv 2>nul
	-$(RMDIR) .pytest_cache 2>nul
	-$(RMDIR) htmlcov 2>nul
	-$(RM) .coverage 2>nul
else
	-$(RMDIR) venv
endif
	@echo "$(GREEN)All generated files removed!$(NC)"

## verify: Verify the built executable exists
verify:
	@echo "$(GREEN)Verifying build...$(NC)"
ifeq ($(DETECTED_OS),Windows)
	@if exist "dist\\$(APP_NAME)$(EXE_EXT)" (echo $(GREEN)Executable found: dist\\$(APP_NAME)$(EXE_EXT)$(NC)) else (echo $(RED)Executable not found!$(NC))
else
	@if [ -f "dist/$(APP_NAME)$(EXE_EXT)" ]; then \
		echo "$(GREEN)Executable found: dist/$(APP_NAME)$(EXE_EXT)$(NC)"; \
		ls -lh "dist/$(APP_NAME)$(EXE_EXT)"; \
	else \
		echo "$(RED)Executable not found!$(NC)"; \
	fi
endif

## release: Prepare for release (clean, test, build, verify)
release: clean-all install test build-quick verify
	@echo "$(GREEN)========================================$(NC)"
	@echo "$(GREEN)Release build completed successfully!$(NC)"
	@echo "$(GREEN)========================================$(NC)"

## dev-setup: Complete development setup
dev-setup: venv install-dev
	@echo "$(GREEN)========================================$(NC)"
	@echo "$(GREEN)Development environment setup complete!$(NC)"
	@echo "$(GREEN)========================================$(NC)"
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Activate virtual environment"
	@echo "  2. Run 'make run' to test the application"
	@echo "  3. Run 'make test' to run tests"

## info: Display project information
info:
	@echo "=========================================="
	@echo "Project Information"
	@echo "=========================================="
	@echo "Application: $(APP_NAME)"
	@echo "Main Script: $(MAIN_SCRIPT)"
	@echo "Test Script: $(TEST_SCRIPT)"
	@echo "Operating System: $(DETECTED_OS)"
	@echo "Python: $(shell $(PYTHON) --version 2>&1)"
	@echo "Pip: $(shell $(PIP) --version 2>&1)"
	@echo "=========================================="
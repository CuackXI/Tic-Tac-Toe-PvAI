# Makefile

.PHONY: setup venv install-env create-env runserver

VENV_PATH=venv
MAIN_FILE=ejecutable.py

venv:
	@echo "🐍 Creando entorno virtual..."
	@python3 -m venv $(VENV_PATH)

install-env:
	@echo "📦 Instalando dependencias..."
	@$(VENV_PATH)/bin/pip install --upgrade pip
	@$(VENV_PATH)/bin/pip install -r requirements.txt

setup: venv install-env

run:
	@$(VENV_PATH)/bin/python $(MAIN_FILE)
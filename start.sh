#!/bin/bash

# Ativar o ambiente virtual
. env/Scripts/activate

# Instalar as dependências
pip install -r requirements.txt

cd clarke

# Criar as migrations e migrar o banco de dados

python manage.py makemigrations
python manage.py migrate

# Iniciar o servidor Django
python manage.py runserver
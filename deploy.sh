#!/bin/bash

# Solicita a mensagem do commit
echo "Digite a mensagem do commit:"
read commit_message

# Verifica se a mensagem do commit foi fornecida
if [ -z "$commit_message" ]; then
    echo "A mensagem do commit é obrigatória!"
    exit 1
fi

# Solicita o nome da branch
echo "Digite o nome da branch:"
read branch_name

# Verifica se o nome da branch foi fornecido
if [ -z "$branch_name" ]; then
    echo "O nome da branch é obrigatório!"
    exit 1
fi

# Cria o arquivo requirements.txt
pip freeze > requirements.txt

# Constrói a imagem Docker
docker build -t clarke .

# Faz commit e push para o GitHub
git add .
git commit -m "$commit_message"
git push origin $branch_name
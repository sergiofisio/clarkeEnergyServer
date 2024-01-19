#!/bin/bash

# Instala a nova dependência
pip install $1

# Atualiza o arquivo requirements.txt
pip freeze > requirements.txt
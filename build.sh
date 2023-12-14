#!/bin/bash

# Сборка Docker-образа
docker-compose build

# Запуск сервисов
docker-compose up -d

echo "Сервис теперь работает по адресу http://127.0.0.1:5000"

# Отслеживание журналов
docker-compose logs -f
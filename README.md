# Steam Games Info

![Python](https://img.shields.io/badge/Python_3.10-blue?logo=python&logoColor=yellow)
![SQLite](https://img.shields.io/badge/SQLite-purple?logo=SQLite&logoColor=blue)
![Docker](https://img.shields.io/badge/Docker-grey?logo=Docker&logoColor=blue)
![DockerCompose](https://img.shields.io/badge/DockerCompose-blue)
![Static Badge](https://img.shields.io/badge/Flask-orange?logo=Flask)

### О проекте
Steam Games Info - это проект, который позволяет извлекать информацию о играх с веб-сайта Steam, такую как название, дата релиза, цена, разработчик и другие данные. Полученные данные записываются в базу данных SQLite. Проект также включает простой веб-интерфейс, который позволяет пользователю обновлять базу данных для игр с первых 15 страниц Steam. После обновления пользователь может просмотреть полученные данные на веб-странице проекта.

### Установка
###### Клонируйте репозиторий: 
    git clone https://github.com/fel1k2/Python-MIPT.git

###### Перейдите в директорию проекта:
    cd Python-MIPT.git

###### Соберите и запустите контейнеры Docker:
    docker-compose up --build

### Технологии

- Язык программирования: Python

- Фреймворк: Flask

- База данных: SQLite

- Docker

###### Структура проекта
    /Python-MIPT
    │
    ├── templates 
    │   └── bd.html
    │   └── filtered_games.html
    │   └── index.html
    │   └── Dockerfile_frontend
    │
    ├── build.sh
    ├── database.py
    ├── docker-compose.yml
    ├── Dockerfile
    ├── flask_backend.py
    ├── parser.py
    └── requirements.txt








### Связь

###### Если у вас есть вопросы или предложения, свяжитесь со мной по электронной почте: zhen.cnyazeff@yandex.ru.

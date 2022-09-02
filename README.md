<h2 align="center">Movies</h2>


Онлайн кинотеатр (backend)


<h2 align="center">Содержание</h2>


1. [Запуск проекта](#запуск-проекта)
   1. [Настройка переменных окружения](#настройка-переменных-окружения)
   2. [Запуск проекта в докере](#запуск-проекта-в-докере)
   3. [Запуск сервисов локально](#запуск-сервисов-локально)
2. [Режим разработки](#режим-разработки)
   1. [Prerequisites](#prerequisites)
   2. [Создание среды разработки](#cоздание-среды-разработки)
   3. [Установка pre-commit хуков](#установка-pre-commit-хуков)
   4. [Управление зависимостями](#управление-зависимостями)
3. [Особенности разработки](#особенности-разработки)
   1. [Структура каталогов](#структура-каталогов)
   2. [Импорты](#импорты)
   3. [Настройки IDE](#настройки-ide)
   4. [Форматер и линтер](#форматер-и-линтер)
4. [Flow работы с проектом](#flow-работы-с-проектом)


<h2 align="center">Запуск проекта</h2>


Все команды, приведенные в данном руководстве, выполняются из корневой директории проекта.

### Настройка переменных окружения
После того как вы создали форк репозитория, нужно создать файлы `.env`.
Для каждого файла `.env` имеется свой файл `.env.template`.

#### Локальные переменные окружения
Создайте файл `.env` в корне проекта - здесь хранятся локальные переменные окружения.
Это переменные хоста, они используются для запуска с помощью docker-compose.

#### Переменные окружения в папке .envs
Папка `.envs` содержит файлы `.env` со всеми переменными окружения, которые используются в проекте.
Здесь есть 2 каталога:
* development - переменные окружения для запуска в режиме разработки;
* production - переменные окружения для запуска в production режиме.

Создайте файлы `.env` в каждом каталоге.

### Запуск проекта в докере
Запуск проекта выполняется с помощью docker-compose. Проект содержит 2 конфигурации docker-compose:
* docker-compose.dev.yml - конфигурация для запуска в режиме разработки;
* docker-compose.prod.yml - конфигурация для запуска в режиме production.

#### Запуск в режиме разработки
Выполните следующую команду для запуска всех сервисов в режиме разработки:
```bash
$ docker-compose -f docker-compose.dev.yml up -d --build
```

#### Запуск в режиме production
Выполните следующую команду для запуска всех сервисов в режиме разработки:
```bash
$ docker-compose -f docker-compose.prod.yml up -d --build
```

### Запуск сервисов локально
Вы можете запустить каждый сервис локально, не используя docker.

#### Запуск сервиса adminpanel
**Важно:** для запуска сервиса `adminpanel` локально у вас должна быть запущена база данных.
Вы можете запустить проект через docker-compose, затем остановить контейнер `adminpanel`,
а затем запустить сервис локально.

Для запуска сервиса `adminpanel` локально перейдите в каталог `adminpanel/src`:
```bash
$ cd adminpanel/src
```
Примените миграции и выполните запуск сервиса:
```bash
$ python manage.py migrate
$ python manage.py runserver
```

#### Перенос данных из sqlite в postgres
Сервис, реализующий перенос данных между базами, находится в каталоге `etl`. Для того чтобы перенести данные из sqlite в postgres, скопируйте файл базы sqlite в каталог `etl/files`.

**Важно**: файл базы данных должен называться `db.sqlite`. Переименуйте файл, если он у вас называется по-другому.

Для запуска переноса данных запустите файл `sqlite_to_pg.py`:
```bash
$ python etl/src/sqlite_to_pg.py
```
Обратите внимание: сервис `sqlite_to_pg` по умолчанию запускается в режиме development,
переменные окружения берутся из файла `.envs/development`. Если вы хотите запустить перенос
в режиме production, то перед запуском файла установите переменной окружения `ENVIRONMENT` значение `production`.


<h2 align="center">Режим разработки</h2>


### Prerequisites
Для успешного развертывания среды разработки вам понадобится:
1. Docker (version ^20.10.17). Если у вас его еще нет, следуйте [инструкциям по установке](https://docs.docker.com/get-docker/);
2. Docker-compose (version ^1.29.2). Обратитесь к официальной документации [для установки](https://docs.docker.com/compose/install/);
3. [Pre-commit](https://pre-commit.com/#install).

Также будет полезным:
1. [Hadolint](https://github.com/hadolint/hadolint) - линтер докер файлов.

### Создание среды разработки
#### 1. Установить пакет libpq-dev
**Важно:** этот пакет нужен для корректной работы `psycopg2`. Без этого пакета `psycopg2` не установится.
```bash
$ sudo apt update
$ sudo apt install libpq-dev
```

#### 2. Установить Poetry
**Linux, macOS, Windows (WSL)**
```bash
$ curl -sSL https://install.python-poetry.org | python3 - --version 1.2.0rc2
```

**Windows (Powershell)**
```bash
> (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py - --version 1.2.0rc2
or
> pip install poetry==1.2.0rc2
```
Необходимо добавить путь к Poetry в переменную `PATH`. Затем перезапустить IDE. Узнать путь к `poetry` можно так:

Linux:
```bash
$ which poetry
```
Windows:
```bash
> where poetry
```

#### 3. Проверить, что Poetry установлен корректно
```bash
$ poetry --version
Poetry (version 1.2.0rc2)
```

#### 4. Создать и активировать виртуальную среду
```bash
$ poetry shell
```

#### 5. Установить зависимости
```bash
$ poetry install
```

#### 6. Установить hadolint (опционально)
```bash
$ sudo wget -O /bin/hadolint https://github.com/hadolint/hadolint/releases/download/v2.10.0/hadolint-Linux-x86_64
$ sudo chmod +x /bin/hadolint
```

### Установка pre-commit хуков
#### 1. Проверка установки pre-commit
Пакет [pre-commit](https://pre-commit.com/) включен в список зависимостей и устанавливается командой `poetry install`. Для проверки корректности установки `pre-commit` нужно выполнить команду:
```bash
$ pre-commit --version
pre-commit 2.20.0
```

#### 2. Установка скриптов git hook
```bash
$ pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

### Управление зависимостями
В качестве пакетного менеджера используется [Poetry version 1.2.0rc2](https://python-poetry.org/docs/1.2/#installation). Для управления зависимостями используются группы (см. файл `pyproject.toml`).

Все основные зависимости располагаются в группе `tool.poetry.dependencies`:
```
[tool.poetry.dependencies]
python = "^3.10"
Django = "^4.1"
```
Добавление основной зависимости:
```bash
$ poetry add pendulum
```
Остальные зависимости делятся на группы. Например, группа `lint` - зависимостей для линтинга:
```
[tool.poetry.group.lint.dependencies]
flake8 = "^5.0.4"
flake8-broken-line = "^0.5.0"
flake8-quotes = "^3.3.1"
pep8-naming = "^0.13.2"
```
Добавление зависимости в конкретную группу (использовать флаг `--group` и название группы):
```bash
$ poetry add pytest --group test
```


<h2 align="center">Особенности разработки</h2>


При разработке необходимо придерживаться установленных правил оформления кода.
В этом разделе вы найдете описание настроек редактора кода, линтеры и форматеры, используемые в проекте,
а также другие особенности, которые необходимо учитывать при разработке.

### Структура каталогов
Проект состоит из набора сервисов. Каждый сервис проекта находится в одноименной папке.
Например, сервис `adminpanel` находится в папке `adminpanel`.

Каталог каждого сервиса должен содержать папку `src` - исходные файлы самого сервиса.
Также в каталоге сервиса могут быть следующие папки:
1. **.envs** - файлы `.env` для разных окружений (dev, prod, etc);
2. **docker** - докер файлы для разных окружений.

### Импорты
Выполняйте импорты из каталогов, вложенных в `src`. Следите, чтобы ваши импорты не начинались с папки `src`. Например, рассмотрим сервис `adminpanel`. Структура каталогов сервиса:
```
movies
├── adminpanel
│   ├── src
│   │   ├── config
│   │   ├── movies
│   │   │   ├── mixins.py
│   │   │   └── models.py
│   │   └── manage.py
│   │── .envs
└── └── docker
```
Файл `mixins.py` приложения `movies` содержит миксин `TimeStampedMixin`. Наша задача - импортировать миксин
из файла `mixins.py` в файле `models.py`.

Неправильно:
```python
from src.movies.mixins import TimeStampedMixin
```
Правильно:
```python
from movies.mixins import TimeStampedMixin
```
Если вы используете PyCharm, то вы можете пометить каталог `src` как `Source Root` (правой кнопкой -> Mark Directory as -> Mark as Source Root),
тогда PyCharm будет корректно добавлять импорты.

Такое использование импортов необходимо для корректной контейнеризации приложения в докере.
Внутри докер-контейнера папка приложения может называться по-другому, например, мы захотим назвать её `app`.
В Dockerfile это будет выглядеть так:
```dockerfile
ARG HOME_DIR=/app
WORKDIR $HOME_DIR

COPY ./src .
```
На хосте каталог называется `src`, а в контейнере `app`. Импорт из `src` приведет к ошибке:
```
ModuleNotFoundError: No module named 'src'
```

### Настройки IDE
Проект содержит файл `.editorconfig` - ознакомьтесь с ним, чтобы узнать какие настройки должны быть в вашем редакторе.

Основное:
* максимальная длина строки: 110;
* отступы: пробелы;
* количество отступов: 4;

### Форматер и линтер
В качестве форматера мы используем [black](https://github.com/psf/black). Конфиг black см. в файле `pyproject.toml` в секции `[tool.black]`.
Линтер - flake8, конфиг находится в файле `setup.cfg`.
<h2 align="center">Flow работы с проектом</h2>


- Форкаем проект
- В своем форке создаем новую ветку, делаем туда коммиты. Название ветки = название issue
- Когда все готово создаем PR в основной репо
- Прикрепляем PR к issue
- Проходим ревью
- Вливаем в ветку main (через squash & merge)
- Оповещаем всех остальных (чтобы они подтянули изменения из main и сразу порешали merge conflict)
<h2 align="center">Movies</h2>


Онлайн кинотеатр (backend)


<h2 align="center">Содержание</h2>


1. [Режим разработки](#режим-разработки)
   1. [Создание среды разработки](#cоздание-среды-разработки)
   2. [Установка pre-commit хуков](#установка-pre-commit-хуков)
2. [Управление зависимостями](#управление-зависимостями)
3. [Flow работы с проектом](#flow-работы-с-проектом)


<h2 align="center">Режим разработки</h2>


### Создание среды разработки
#### 1. Установить Poetry

**Linux, macOS, Windows (WSL)**
```bash
> curl -sSL https://install.python-poetry.org | python3 - --version 1.2.0rc2
```

**Windows (Powershell)**
```bash
> (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py - --version 1.2.0rc2
```
Необходимо добавить путь к Poetry (`C:\Users\your-user-name\AppData\Roaming\Python\Scripts`) в переменную `PATH`. Затем перезапустить IDE.

#### 2. Проверить, что Poetry установлен корректно
```bash
> poetry --version
Poetry (version 1.2.0rc2)
```
#### 3. Создать и активировать виртуальную среду
```bash
> poetry shell
```
#### 4. Установить зависимости
```bash
> poetry install
```

### Установка pre-commit хуков

#### 1. Проверка установки pre-commit
Пакет [pre-commit](https://pre-commit.com/) включен в список зависимостей и устанавливается командой `poetry install`. Для проверки корректности установки `pre-commit` нужно выполнить команду:
```bash
> pre-commit --version
pre-commit 2.20.0
```

#### 2. Установка скриптов git hook
```bash
> pre-commit install
pre-commit installed at .git/hooks/pre-commit
```


<h2 align="center">Управление зависимостями</h2>


В качестве пакетного менеджера используется [Poetry version 1.2.0rc2](https://python-poetry.org/docs/1.2/#installation). Для управления зависимостями используются группы (см. файл `pyproject.toml`).

Все основные зависимости располагаются в группе `tool.poetry.dependencies`:
```
[tool.poetry.dependencies]
python = "^3.10"
Django = "^4.1"
```
Добавление основной зависимости:
```bash
> poetry add pendulum
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
> poetry add pytest --group test
```


<h2 align="center">Flow работы с проектом</h2>


- Форкаем проект
- В своем форке создаем новую ветку, делаем туда коммиты. Название ветки = название issue
- Когда все готово создаем PR в основной репо
- Прикрепляем PR к issue
- Проходим ревью
- Вливаем в ветку main (через squash & merge)
- Оповещаем всех остальных (чтобы они подтянули изменения из main и сразу порешали merge conflict)

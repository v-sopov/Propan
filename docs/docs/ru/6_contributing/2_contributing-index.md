# Разработка

Если вы уже склонировали репозиторий и уверены, что хотите погрузить в код, вам пригодятся эти гайдлайны для настройки окружения.

### Создайте окружение `venv`

Как и любой *python* проект, **Propan** лучше разрабатывать в отдельном окружении.
Вы можете создать его с пумощью встроенного в *python* модуля `venv`:

```bash
python -m venv venv
```

Эта команда создаст директорию `./venv/`, куда вы сможете изолированно установить все зависимости проекта.

### Активируйте окружение

Активируйте созданное окружение следующей командой:

```bash
source ./venv/bin/activate
```

И удостоверьтесь, что вы используете последнюю версию `pip`'а

```bash
python -m pip install --upgrade pip
```

### pip

После активации окружения установите все зависимости проекта, необходимые для разработки

```bash
pip install -e ."[dev]"
```

#### Используйте ваш локальный Propan

Если вы создадите новый *Python* файл и импортируете там **Propan**, он будет использовать **Propan** из вашей локальной директории проекта.

И, если вы обновите код вашего локального **Propan**, изменения будут отражены в работе вашего локального *Python* файла, т.к. проект был установлен с флагом `-e`.

Таким образом, вам не нужно "устанавливать" локальную версию фреймворка после каждого изменения в его репозитории.

Для использования локального `CLI` необходима следующая команда:

```bash
python -m propan ...
```

### Тестирование

#### Pytests

Для запуска тестов с вашим текущим Python и окружением используйте стандартный pytest или один из заготовленных скриптов

```bash
pytest tests
# or
bash ./scripts/test.sh
# with coverage output
bash ./scripts/test-cov.sh
```

В проекте используется нескольо *pytest marks*:

* **slow**
* **rabbit**
* **nats**
* **all**

!!! tip ""
    Больше узнать про маркировку тестов вы можете [здесь](https://docs.pytest.org/en/7.1.x/example/markers.html)

По умолчанию *pytest* запускается с тегом "not slow".

Для запуска всех тестов используйте:

```bash
pytest -m 'all'
```

Если вы не запустили RabbiMQ и NATS у себя локально, вы можеет запустить тесты без этих зависимостей:

```bash
pytest -m 'not rabbit and not nats'
```

Для запуска всех тестов со всеми зависимостями, сначала запустите *docker-compose.yml*

```bash
docker compose up -d
```

со следующим содержанием

```yaml
version: "3"

services:
  rabbit:
    image: rabbitmq
    ports:
      - 5672:5672
  
  nats:
    image: nats
    ports:
      - 4222:4222
```

#### Hatch

Если вы используете **hatch** для управления окружением, в проекте есть несколько команда для него:

##### **TEST**

Это окружение запускает тесты на всех поддерживаемых версиях python: 3.7-3.11

!!! note
    Все версии языка должны быть установлены на вашей системе

```bash
# Запустить минимальный набор тестов на python3.7-3.11
hatch run test:run

# Запустить все тесты на python3.7-3.11
hatch run test:run-all
```

##### **TEST-LAST**

Это окружение запускает тесты на версии python 3.11

```bash
# Запустить минимальный набор тестов на python3.11
hatch run test-last:run

# Запустить все тесты на python3.11
hatch run test-last:run-all

# Запустить все тесты на python3.11 с измерением покрытия
hatch run test-last:cov
```

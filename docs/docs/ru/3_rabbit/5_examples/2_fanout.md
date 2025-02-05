# Fanout Exchange

**Fanout** Exchange - еще более простой, но чуть менее популярный способ маршрутизации в *RabbitMQ*. Данный тип `exchange` отправляет сообщения
во все очереди, подписанные на него, игнорируя любые аргументы самого сообщения.

При этом, если очередь слушает несколько потребителей, сообщения все также будут распределяться между ними.

## Пример

```python linenums="1"
{!> docs_src/rabbit/examples/fanout.py !}
```

### Объявление потребителей

Для начала мы объявили наш **Fanout** exchange и несколько очередей, которые будут его слушать:

```python linenums="8" hl_lines="1"
{!> docs_src/rabbit/examples/fanout.py [ln:8-11]!}
```

Затем мы подписали несколько потребителей с помощью объявленных очередей на созданный нами `exchange`

```python linenums="13" hl_lines="1 5 9"
{!> docs_src/rabbit/examples/fanout.py [ln:13-23]!}
```

!!! note
    Обратите внимание, что `handler1` и `handler2` подписаны на один `exchange` с помощью одной и той же очереди:
    в рамках одного сервиса это не имеет смысла, так как сообщения будут приходить в эти обработчики поочередно.
    Здесь мы эмулируем работу несколько потребителей и балансировку нагрузки между ними.

### Распределение сообщений

Теперь распределение сообщений между этими потребителями будет выглядеть следующим образом:

```python
{!> docs_src/rabbit/examples/fanout.py [ln:29]!}
```

Сообщений `1` будет отправлено в `handler1` и `handler3`, т.к. они слушает `exchange` с помощью разных очередей

---

```python
{!> docs_src/rabbit/examples/fanout.py [ln:30]!}
```

Сообщений `2` будет отправлено в `handler2` и `handler3`, т.к. `handler2` слушает `exchange` с помощью той же очереди, что и `handler1`

---

```python
{!> docs_src/rabbit/examples/fanout.py [ln:31]!}
```

Сообщений `3` будет отправлено в `handler1` и `handler3`

---

```python
{!> docs_src/rabbit/examples/fanout.py [ln:32]!}
```

Сообщений `4` будет отправлено в `handler3` и `handler3`

---

!!! note
    При отправке сообщений в **Fanout** exchange нет смысл указывать аргументы `queue` или `routing_key`, т.к. они будут проигнорированы
Важно! Проект не готовый, возможны баги, недоделал маленько
# Тестовое задание

В рамках данного тестового задания решено разделить сервис на три компонента для обеспечения максимальной масштабируемости и эффективности работы:

- Сервис 'app' — клиентское приложение для добавления устройств в базу данных и регистрации пользователей.
- Сервис 'metrics' — предназначен для загрузки данных с устройств.
- Сервис 'analytic' — осуществляет анализ данных, полученных из базы.

## Инфраструктура

В качестве хранилища данных для устройств и пользователей используется Postgres SQL. Для автоматизации работы с временными метками выбрана база данных Influx DB, способствующая эффективному извлечению данных за заданные периоды времени и обладающая высокой скоростью записи. В качестве брокера сообщений применяется RabbitMQ.

Автоматическое создание таблиц в Postgres производится при загрузке Docker-контейнера с использованием файла init.sql. Остальные базы данных также используют отдельные Docker-контейнеры с минимально необходимым набором настроек.

Для подключения к базам данных временно используется прямое указание параметров подключения. Для подключения к InfluxDB требуется токен, который должен быть указан в настройках среды сервиса 'analytic'.

## Общие сведения
Разделение на сервисы позволяет устройствам взаимодействовать с одним API изолированно. Масштабирование сервиса достигается путем запуска нескольких его реплик. Сервисы 'app' и 'analytic' могут быть объединены, так как изначально предполагалось, что в 'app' будут реализованы конечные точки для получения аналитики.

Для передачи задач аналитики используется Celery. Это требует запуска отдельных компонентов: analysis_worker для обработки задач аналитики и app.py для обработки пользовательских запросов с использованием сервера Uvicorn.

## Запуст
Для успешного запуска проекта необходимо инициализировать в общей сложности шесть Docker-контейнеров, поскольку предполагается, что сервисы функционируют независимо друг от друга:

- Три базы данных, для каждой из которых требуется отдельный контейнер. Контейнеры для баз данных можно настроить, используя соответствующие директории из docker/db_name.
- Три сервиса, каждый из которых также требует своего контейнера.
Для настройки подключения каждого из сервисов к соответствующей базе данных используется файл config.json. Для базы данных InfluxDB необходимо дополнительно создать и указать токен для подключения.

В случае локального запуска следует учесть, что Docker-контейнеры не могут взаимодействовать через localhost напрямую. Для обеспечения коммуникации между контейнерами необходимо настроить кастомную сеть в Docker. 

## Необходимые дополнения
Проект требует доработки в нескольких направлениях:

- Реализация обработки ошибок во всех компонентах.
- Создание конфигурационных файлов для упрощения подключения к базам данных.
- Добавление комментариев и документации для лучшего понимания кода.
- Реализация Docker-контейнеров для всех сервисов.
- Тестирование - модульные, интеграционные, нагрузочные 

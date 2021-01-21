# Foodgram

Foodgram — социальная сеть для любителей вкусно покушать. Публикуйте рецепты, подписывайтесь на авторов, составляйте списки покупок.

[Демо доступно по этому адресу](http://130.193.51.183/)

## Зависимости

Установите Docker с [официального сайта](https://www.docker.com/).

## Запуск сервиса

Убедитесь, что Docker установлен и запущен.

Склонируйте репозиторий 
```
git clone https://github.com/jlllk/foodgram-project.git
```
В корне проекта скопируйте .env.template и назовите новый файл .env
```
cp .env.template .env
```
Заполните шаблон по этому примеру
```
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY= # секретный ключ ваше проекта на Джанго
ALLOWED_HOSTS= # разрешенные хосты
```
Запустите проект
```
docker-compose up
```
Выполните первые миграции
```
docker exec -ti web python manage.py migrate
```
Создайте суперпользователя
```
docker exec -ti web python manage.py createsuperuser
```
При желании вы можете загрузить тестовый набор данных из папки fixtures
```
docker exec -ti web python manage.py loaddata <path>
```

## Использованные технологии

* [Python](https://www.python.org/) - Язык программирования
* [Django](https://www.djangoproject.com/) - Веб-фреймворк
* [PostgreSQL](https://www.postgresql.org/) - Реляционная база данных

## Автор

* [Шильцин Станислав](https://github.com/jlllk)

## Лицензия
Данный проект распростарняется под Лицензией MIT.

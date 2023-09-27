# Foodgram Project
## Описание проекта

«Фудграм» — сайтом, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов.
Пользователям сайта также доступен сервис «Список покупок». Он позволяет создавать список продуктов, которые нужно купить для приготовления выбранных блюд.
У веб-приложения уже есть готовый фронтенд — это одностраничное SPA-приложение, написанное на фреймворке React. Файлы, необходимые для его сборки, хранятся в папке frontend. 

## Схема работы веб-приложения

Проект состоит из следующих страниц: 
- **главная** -- список первых шести рецептов, отсортированных по дате публикации «от новых к старым». На этой странице реализована постраничная пагинация. Остальные рецепты доступны на следующих страницах.
- **страница рецепта** -- полное описание рецепта. У авторизованных пользователей есть возможность добавить рецепт в избранное и список покупок, а также подписаться на автора рецепта.
- **страница пользователя** -- отображается имя пользователя, все рецепты, опубликованные пользователем и возможность подписаться на пользователя.
- **страница подписок** -- список рецептов, опубликованных теми авторами, на которых пользователь подписался. Записи сортируются по дате публикации — от новых к старым.
- **избранное** -- список избранных рецептов пользователя
- **список покупок** -- список рецептов, добавленных в «Список покупок». Пользователь может нажимать кнопку «Скачать список» и получить файл с перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».
- **создание и редактирование рецепта** -- пользователь может создать или отредактировать любой рецепт, который он создал.

## Как работает проект

Backend проекта реализован на Django и использует базу данных PostgreSQL.
Проект запускается в трёх контейнерах — nginx, PostgreSQL и Django через docker-compose (контейнер frontend используется лишь для подготовки файлов).
Образы проекта запушены на Docker Hub.
Проект доступен по ссылке: [Сайт проекта](https://foodgram-as.sytes.net/)

## Как запустить

Для запска необходим установленный Docker. Убедитесь, что он запущен.
Для выполнения шагов, истользуйте терминал.
1. Клонируйте репозиторий к себе на компьютер.
    ```bash
    git clone git@github.com:cry-cry142/foodgram-project-react.git
    ```

2. В папке проекта выполните команду: 
    - для сборки контейнеров из DockerHub:
        ```bash
        docker compose -f docker-compose.production.yml up
        ```
    - для сборки из локальных файлов:
        ```bash
        docker compose up
        ```

3. Выполните миграции.
    ```bash
    sudo docker compose [-f docker-compose.production.yml] exec backend python manage.py migrate
    ```

4. Соберите статику и копируйте её.
    ```bash
    sudo docker compose [-f docker-compose.production.yml] exec backend python manage.py collectstatic
    sudo docker compose [-f docker-compose.production.yml] exec backend cp -r /app/collected_static/. /backend_static/backend_static/
    ```

## Пример запросов API
**[POST] http://<hostname>/api/users/**

*Request samples*
```json
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
```
*Response samples*
```json
{
  "email": "vpupkin@yandex.ru",
  "id": 0,
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин"
}
```

**[GET] http://<hostname>/api/recipes/**

*Response samples*
```json
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

Полную документацию можно найти [тут](https://foodgram-as.sytes.net/api/redoc/)

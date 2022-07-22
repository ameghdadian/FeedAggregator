# DKChallenge

## Initial project setup
 - Create a `.env` file with the following content at the root project directory:
  ```
    FEED_CELERY_QUEUE = 'feed_tasks'
  ```
 - Run `docker-compose build` through terminal,
 - Run `docker-compose run --rm app sh -c 'python manage.py fillfeedsource'` to fill the initial feed sources table,
  - Run `docker-compose up`

## Run tests
You can run the tests by executing following command in terminal:
```shell
    docker-compose run --rm app sh -c 'python manage.py test && flake8'
```


## App Modules Summary
 - **app** module contains whole project setting.
 - **comment** module have the necessary endpoints to display a feed's comment and submit a comment on a field.
 - Inside **core** module you can find all the models utilized inside this project.
 - **feed** module holds the functionality to display feed items.
 - By using endpoints provided inside **feedsource**, you can follow a FeedSource.
    > FeedSource is the destination from which feed items are retrieved.
 - **user** module contains necessary functionality to create and authenticate a user.



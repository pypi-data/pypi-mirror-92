# После установки

Добавить приложение в список INSTALLED_APPS проекта:
```python
INSTALLED_APPS = [
    ...
    'sso_client'
]
```

Выполнить миграции:
```shell
python manage.py migrate
```

Добавить в settings.py следующие строки:
```python
# settings for sso login
AUTH_USER_MODEL = 'sso_client.OauthUser'
AUTHENTICATION_BACKENDS = ('sso_client.backends.TokenAuth', )
SSO_URL = '{адрес sso сервера}/sso/'
```

Добавить в секцию middleware:
```python
'sso_client.middleware.CheckTokenMiddleware',
'sso_client.middleware.AuthMiddleware'
```
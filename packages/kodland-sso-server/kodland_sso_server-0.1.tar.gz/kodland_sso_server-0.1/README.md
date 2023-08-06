# После установки

Добавить приложение в список **INSTALLED_APPS** в settings.py
```python
INSTALLED_APPS = [
    ...
    'sso_server'
]
```

Выполнить миграции:
```shell
python manage.py migrate
```

**Добавить в settings.py в middleware:**
```'sso_server.middleware.UserCookieMiddleWare'```

Добавить в urls.py следующий маршрут:

```python
urlpatterns = [
    ...
    path('sso/', include('sso_server.urls'))
]
```
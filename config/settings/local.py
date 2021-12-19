from .base import *

ALLOWED_HOSTS = []

""" SQLite 접속 방식 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""

""" Local MySQL """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 사용하려는 DB 이름
        'NAME': 'mysite',
        # 여기부터 connection 정보
        'USER' : 'mysite',
        'PASSWORD' : '1qaz!QAZ',
        'HOST' : '127.0.0.1',
        'PORT' : '3306',
    }
}
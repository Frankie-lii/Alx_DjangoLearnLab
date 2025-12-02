# Database configuration for SQLite with PostgreSQL parameters commented
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'USER': '',  # SQLite doesn't use these parameters
        'PASSWORD': '',  # SQLite doesn't use these parameters
        'HOST': '',  # SQLite doesn't use these parameters
        'PORT': '',  # SQLite doesn't use these parameters
    }
}

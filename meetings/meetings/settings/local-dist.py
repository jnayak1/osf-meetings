"""Copy this file into local.py for local development"""


SECRET_KEY = ''  # Set to large random value in your local.py
DEBUG = True
CLIENT_ID = ''
CLIENT_SECRET = ''
MAILGUN_API_KEY = ''
ANYMAIL = {
    "MAILGUN_API_KEY": MAILGUN_API_KEY,
}

# Database
# POSTGRES_NAME = ''
# POSTGRES_USER = ''
# POSTGRES_PASSWORD = ''
# POSTGRES_HOST = ''
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': POSTGRES_NAME,
#         'USER': POSTGRES_USER,
#         'PASSWORD': POSTGRES_PASSWORD,
#         'HOST': POSTGRES_HOST,
#         'PORT': '',
#     }
# }

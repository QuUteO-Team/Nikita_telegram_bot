import contextlib
import os

with contextlib.suppress(ImportError):
    from dotenv import load_dotenv

    load_dotenv()


PAID_USERS = []

PERMISSIONS = ['permissions.PaywallPermission']


ADMIN_GROUP = [] # here is tg id

HIDERS_CHECKER = 'hiders_checker.DemoHidersChecker'


REDIS_PERSISTENCE = { # redis isn't work

    'HOST': '127.0.0.1',

    'PORT': 6379,

    'DB': 0,

    'PASSWORD': None,
}

TOKEN = os.getenv('TOKEN', '')

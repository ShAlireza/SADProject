import os
from tortoise import Tortoise

NAMESPACE_USER = os.getenv("SERVICE_USER")
PYTHONPATH = os.getenv("PYTHONPATH")
DATABASE_URL = os.getenv("DATABASE_URL")
HOST = os.getenv("HOST", 'payment.alantouring.ir')
ZARINPAL_CALLBACK_PATH = os.getenv(
    'ZARINPAL_CALLBACK_PATH', '/zarinpal'
)
ZARINPAL_CALLBACK = f"https://{HOST}{ZARINPAL_CALLBACK_PATH}"
ZARINPAL_MERCHANT_ID = os.getenv("ZARINPAL_MERCHANT_ID")
ZARINPAL_CLIENT = os.getenv("ZARINPAL_CLIENT")
ZARINPAL_START_PAY = os.getenv("ZARINPAL_START_PAY")
AUTHORIZATION_URL = os.getenv(
    "AUTHORIZATION_URL", "http://accounts.accounts/token"
)


TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "payment": {
            "models": ["data.db.models", 'aerich.models'],
            "default_connection": "default",
        }
    }
}

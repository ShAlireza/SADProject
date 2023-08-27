import os

SERVICE_USER_USER = os.getenv("SERVICE_USER")
PYTHONPATH = os.getenv("PYTHONPATH")
DATABASE_URL = os.getenv("DATABASE_URL")
AUTHORIZATION_URL = os.getenv(
    "AUTHORIZATION_URL", "https://accounts.alantouring.ir/token"
)

TOUR_API = os.getenv("TOUR_API", "http://tour-api.tour")
PAYMENT_API = os.getenv("PAYMENT_API", "http://payment.backend")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "cart": {
            "models": ["data.db.models", 'aerich.models'],
            "default_connection": "default",
        }
    }
}

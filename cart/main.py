from fastapi import FastAPI

from routers import cart_router


app = FastAPI()

app.include_router(
    cart_router,
    tags=['Cart']
)

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from propan.fastapi import RabbitRouter

app = FastAPI()

router = RabbitRouter("amqp://guest:guest@localhost:5672")


class Incoming(BaseModel):
    m: dict


def call():
    return True


@router.event("test")
async def hello(m: Incoming, d=Depends(call)) -> dict:
    return {"response": "Hello, world!"}


@router.get("/")
async def hello_http():
    return "Hello, http!"


app.include_router(router)

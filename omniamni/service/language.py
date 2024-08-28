import uvicorn
from fastapi import Body, FastAPI
from pydantic import BaseModel

from omniamni.model import SimpleText, SimpleBool

app = FastAPI()


@app.get("/is_bad_language")
async def is_bad_language(text: SimpleText):
    return SimpleBool(value=False)


async def start():
    port =
    config = uvicorn.Config("main:app", port=, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

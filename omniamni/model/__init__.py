from pydantic import BaseModel


class SimpleBool(BaseModel):
    value: bool


class SimpleText(BaseModel):
    value: str

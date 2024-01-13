from pydantic import BaseModel

from chat_chart.pollution.entities import Result


class QueryBody(BaseModel):
    text: str


class QueryResponse(BaseModel):
    result: Result

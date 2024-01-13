from pydantic import BaseModel


class ResultTable(BaseModel):
    headers: list[str]
    data: list[list[str | float | int | bool]]


class Result(BaseModel):
    text: str
    sql: str
    table: ResultTable

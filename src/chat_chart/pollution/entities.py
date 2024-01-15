from pydantic import BaseModel


class ResultTable(BaseModel):
    headers: list[str]
    rows: list[list[str | float | int | bool | None]]


class ResultChart(BaseModel):
    pass


class Result(BaseModel):
    text: str
    sql: str | None
    table: ResultTable | None
    chart: ResultChart | None

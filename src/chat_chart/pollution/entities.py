from enum import StrEnum, auto

from pydantic import BaseModel


class ResultTable(BaseModel):
    headers: list[str]
    rows: list[list[str | float | int | bool | None]]


class ChartType(StrEnum):
    SCATTER = auto()
    BAR = auto()
    LINE = auto()


class ResultChart(BaseModel):
    type: ChartType
    config: dict


class Result(BaseModel):
    text: str
    sql: str
    table: ResultTable
    chart: ResultChart | None


class ColumnType(StrEnum):
    NUMBER = auto()
    AGGREGATION = auto()
    YEAR = auto()
    STRING = auto()
    LOCATION = auto()
    OTHER = auto()


class ColumnStats(BaseModel):
    name: str
    type: ColumnType
    is_unique: bool
    n_values: int
    has_null: bool

    def is_numerical(self) -> bool:
        return self.type in [
            ColumnType.NUMBER,
            ColumnType.AGGREGATION,
            ColumnType.YEAR,
        ]

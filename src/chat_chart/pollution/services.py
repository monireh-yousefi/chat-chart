from collections import defaultdict

from pydantic import BaseModel

from chat_chart.llm.entities import LLMMessage, LLMMessageRole
from chat_chart.llm.services import LLMService
from chat_chart.pollution.entities import ResultTable, ColumnStats, ColumnType, ResultChart, ChartType
from chat_chart.pollution.repositories import PollutionRepository


class PollutionService:
    def __init__(
            self,
            llm_service: LLMService,
            pollution_repository: PollutionRepository,
    ):
        self._llm_service = llm_service
        self._pollution_repository = pollution_repository

    async def get_sql(self, text: str) -> str:
        return await self._llm_service.query(
            messages=[
                LLMMessage(
                    role=LLMMessageRole.SYSTEM,
                    content='You are a SQL query generator for pollution submissions table.\n' \
                            'The query should consist of a single SELECT statement.\n' \
                            'The table name is `pollution_submissions` and it contains amount of pollution through different years and different cities.\n' \
                            'The table contains the following fields:\n' \
                            '"region": A text field containing the region of submission.\n' \
                            '"iso3": A text field containing ISO3 code of the country.\n' \
                            '"country": A text field containing the country of submission.\n' \
                            '"city": A text field containing the city of submission.\n' \
                            '"year": A integer field containing the year of submission.\n' \
                            '"pm25": Float field containing amount of PM2.5 which is particle pollution from fine particulates.\n' \
                            '"pm10": Float field containing amount of particles with a diameter of 10 micrometers or less.\n' \
                            '"no2": Float field containing amount of nitrogen in the air.'
                ),
                LLMMessage(
                    role=LLMMessageRole.USER,
                    content=f'Generate a SQL query for the following message:\n {text}'
                ),
            ]
        )

    async def get_table(self, sql: str) -> ResultTable:
        return await self._pollution_repository.run_sql(
            sql=sql,
        )

    async def get_chart(self, table: ResultTable) -> ResultChart | None:
        stats = self._get_column_stats(table=table)
        """
        * if we have less than 2 columns -> null
        
        bar:
            if: we have at 1 column that is unique and n_values is low
                we have another column that is a number / aggregate.
            1. select the unique column as x
            2. select the other column as y
            
        line:
            if: we have (at least) 1 column that is unique
                we have (at least) one other column
            1. select the unique field as x (and set labels)
            2. select the other column as y
            
        scatter: 
            if: we have (at least) two numeric or aggregation columns
            1. select first numeric column as x
            2. select second numeric column as y
        """

        if len(stats) < 2:
            return None

        df_format_rows = []
        for row in table.rows:
            df_row = {}
            for i, val in enumerate(row):
                df_row[table.headers[i]] = val

            df_format_rows.append(df_row)

        class DFTable(BaseModel):
            headers: list[str]
            rows: list[dict]

        df_table = DFTable(headers=table.headers, rows=df_format_rows)

        # bar:
        x_col = None
        y_col = None
        for stat in stats:
            if not x_col and stat.is_unique and stat.n_values < 20:
                x_col = stat
                continue

            if not y_col and stat.is_numerical():
                y_col = stat
                continue

        if x_col and y_col:
            config = {
                'type': 'bar',
                'data': {
                    'labels': [],
                    'datasets': [{
                        'label': 'Bar Chart',
                        'data': [],
                        'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                        'borderColor': 'rgb(255, 99, 132)',
                        'borderWidth': 1
                    }]
                },
                'options': {}
            }

            for row in df_table.rows:
                config['data']['labels'].append(row[x_col.name])
                config['data']['datasets'][0]['data'].append(row[y_col.name])

            return ResultChart(
                type=ChartType.BAR,
                config=config,
            )

        # line:
        x_col = None
        y_col = None
        for stat in stats:
            if not x_col and stat.is_unique:
                x_col = stat
                continue

            if not y_col and stat.is_numerical():
                y_col = stat
                continue

        if x_col and y_col:
            sorted_df_table_rows = sorted(df_table.rows, key=lambda x: x[x_col.name])
            config = {
                'type': 'line',
                'data': {
                    'labels': [],
                    'datasets': [{
                        'label': 'Line Chart',
                        'data': [],
                        'fill': False,
                        'borderColor': 'rgb(75, 192, 192)',
                    }]
                },
                'options': {}
            }

            for row in sorted_df_table_rows:
                config['data']['labels'].append(row[x_col.name])
                config['data']['datasets'][0]['data'].append(row[y_col.name])

            return ResultChart(
                type=ChartType.LINE,
                config=config,
            )

        # scatter:
        x_col = None
        y_col = None
        for stat in stats:
            if not x_col and stat.type in [ColumnType.NUMBER, ColumnType.AGGREGATION]:
                x_col = stat
                continue

            if not y_col and stat.type in [ColumnType.NUMBER, ColumnType.AGGREGATION]:
                y_col = stat
                continue

        if x_col and y_col:
            config = {
                'type': 'scatter',
                'data': {
                    'datasets': [{
                        'label': 'Scatter Chart',
                        'data': [],
                        'backgroundColor': 'rgb(255, 99, 132)'
                    }]
                },
                'options': {}
            }

            for row in df_table.rows:
                config['data']['datasets'][0]['data'].append({
                    'x': row[x_col.name],
                    'y': row[y_col.name],
                })

            return ResultChart(
                type=ChartType.SCATTER,
                config=config,
            )

        return None

    def _get_column_stats(self, table: ResultTable) -> list[ColumnStats]:
        column_data = [list() for _ in table.headers]
        for row in table.rows:
            for i, value in enumerate(row):
                column_data[i].append(value)

        stats = []
        for i, cd in enumerate(column_data):
            stat = ColumnStats(
                name=table.headers[i],
                type=ColumnType.NUMBER,
                is_unique=False,
                n_values=0,
                has_null=False,
            )

            values = set(cd)
            if len(values) == len(cd):
                stat.is_unique = True
            stat.n_values = len(values)
            stat.has_null = None in values

            col_types_num = defaultdict(lambda: 0)
            for value in values:
                if type(value) == str:
                    if any(c in stat.name.lower() for c in ['country', 'city', 'region']):
                        col_types_num[ColumnType.LOCATION] += 1
                    else:
                        col_types_num[ColumnType.STRING] += 1
                elif type(value) in (int, float):
                    if any(c in stat.name.lower() for c in ['sum', 'avg', 'count', 'max', 'min']):
                        col_types_num[ColumnType.AGGREGATION] += 1
                    elif type(value) == int and 1800 < value < 2100:
                        col_types_num[ColumnType.YEAR] += 1
                    else:
                        col_types_num[ColumnType.NUMBER] += 1
                else:
                    col_types_num[ColumnType.OTHER] += 1

            stat.type = max(col_types_num.keys(), key=lambda x: col_types_num[x])

            stats.append(stat)

        return stats

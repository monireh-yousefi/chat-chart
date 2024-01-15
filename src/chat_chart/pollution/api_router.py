from typing import Annotated

import sqlparse
from fastapi import APIRouter, Request, Body, Form
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from chat_chart.pollution.entities import Result
from chat_chart.pollution.schemas import QueryBody, QueryResponse

router = APIRouter(tags=['pollution'])


@router.post('/api/v1/pollution/query')
async def query(
        request: Request,
        body: Annotated[QueryBody, Body()],
):
    service = request.app.state.container.pollution_service

    sql = await service.get_sql(text=body.text)
    table = await service.get_table(sql=sql)
    chart = await service.get_chart(table=table)

    return QueryResponse(
        result=Result(
            text=body.text,
            sql=sql,
            table=table,
            chart=chart,
        )
    )


@router.get('/ui/v1/pollution/home')
async def get_home(
        request: Request,
) -> HTMLResponse:
    config = request.app.state.container.config

    templates = Jinja2Templates(
        directory=config.project_path / 'src/templates',
    )

    return templates.TemplateResponse(
        request=request,
        name='home.html',
        context={},
    )


@router.post('/ui/v1/pollution/result')
async def get_result(
        request: Request,
        text_query: Annotated[str, Form()]
) -> HTMLResponse:
    config = request.app.state.container.config
    service = request.app.state.container.pollution_service

    sql = await service.get_sql(text=text_query)
    table = await service.get_table(sql=sql)
    chart = await service.get_chart(table=table)

    templates = Jinja2Templates(
        directory=config.project_path / 'src/templates',
    )

    if sql:
        sql = sqlparse.format(sql, reindent=True, keyword_case='upper')

    return templates.TemplateResponse(
        request=request,
        name='result.html',
        context=Result(
            text=text_query,
            sql=sql,
            table=table,
            chart=chart,
        ).model_dump(),
    )

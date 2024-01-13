from typing import Annotated

from fastapi import APIRouter, Request, Body

from chat_chart.pollution.schemas import QueryBody, QueryResponse

router = APIRouter(prefix='/pollution', tags=['pollution'])


@router.post('/query')
async def query(
        request: Request,
        body: Annotated[QueryBody, Body()],
):
    service = request.app.state.container.pollution_service
    return QueryResponse(
        data=await service.get_query_data(message=body.message),
        chart=await service.get_query_chart(message=body.message),
    )

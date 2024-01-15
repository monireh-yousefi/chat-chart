from fastapi import APIRouter
from starlette.responses import RedirectResponse

router = APIRouter()


@router.get('/')
async def get_index() -> RedirectResponse:
    return RedirectResponse(url='/ui/v1/pollution/home')

from fastapi import APIRouter

router = APIRouter(
    prefix="/query",
    tags=["Query"],
)


@router.post("")
async def query():
    return {
        "message": "Not implemented yet"
    }
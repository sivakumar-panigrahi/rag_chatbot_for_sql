from fastapi import APIRouter

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback"],
)


@router.post("")
async def feedback():
    return {
        "message": "Feedback received"
    }
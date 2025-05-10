from fastapi import APIRouter
from starlette import status

from ..utils.depends import db_dependency, user_dependency
from ..schemas.event import EventRequest

from ..services.event import create_event_service


router = APIRouter(
    prefix="/event",
    tags=["event"],
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_event(user: user_dependency, event_request: EventRequest, db: db_dependency):
    event = create_event_service(user, event_request, db)
    return event
        
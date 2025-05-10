from fastapi import HTTPException
from starlette import status
from datetime import datetime, timezone 

from ..utils.depends import db_dependency, user_dependency
from ..schemas.event import EventRequest
from ..models.models import Events


def create_event_service(user: user_dependency, event_request: EventRequest, db: db_dependency) -> Events:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized")
    
    event_model = Events(
        **event_request.model_dump(), 
        created_by=user.get("id"),
        update_at = datetime.now(timezone.utc)
    )
    db.add(event_model)
    db.commit()
    db.refresh(event_model)
    return event_model

from pydantic import BaseModel, Field, ConfigDict, UUID4
from typing import Optional, List
from datetime import datetime

class SprintCreateRequest(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime

class SprintUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class SprintResponse(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    model_config = ConfigDict(from_attributes=True)


class SprintListResponse(BaseModel):
    sprints: List[SprintResponse]
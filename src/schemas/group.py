from pydantic import BaseModel, Field, ConfigDict, UUID4
from typing import Optional, List


class GroupCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class GroupUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class GroupResponse(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class GroupListResponse(BaseModel):
    groups: List[GroupResponse]
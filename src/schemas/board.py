from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class BoardCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class BoardUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class BoardResponse(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)


class BoardListResponse(BaseModel):
    boards: List[BoardResponse]
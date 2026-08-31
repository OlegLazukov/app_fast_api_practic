from pydantic import BaseModel, Field, ConfigDict, UUID4
from typing import Optional, List


class ColumnCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    board_id: UUID4 | None = None

class ColumnUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    board_id: Optional[UUID4] = None



class ColumnResponse(BaseModel):
    name: str
    board_id: UUID4 | None = None
    model_config = ConfigDict(from_attributes=True)

class ColumnListResponse(BaseModel):
    columns: List[ColumnResponse]
from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    detail: str
    error_code: str


class SuccessResponse(BaseModel):
    message: str
    data: Any = None  # You can include any additional data here, e.g., project_id or other details


class ProjectDetailResponse(BaseModel):
    id: str = Field(..., description="The unique identifier of the project")
    name: str = Field(..., description="The name of the project")
    description: Optional[str] = Field(None, description="A brief description of the project")
    created_by: str = Field(..., description="The username of the creator")
    created_at: datetime = Field(..., description="The timestamp when the project was created")

class GetProjectsResponse(BaseModel):
    message: str = Field(..., description="The status message of the API response")
    projects: List[ProjectDetailResponse] = Field(..., description="A list of projects with their details")
    total_project: int  # Add this field
    page: int  # Add this field
    page_size: int  # Add this field
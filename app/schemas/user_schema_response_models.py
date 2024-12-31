from pydantic import BaseModel, Field
from typing import Optional, List

class SuccessResponse(BaseModel):
    message: str = Field(..., example="Operation completed successfully.") # type: ignore

class UserRegistrationResponse(SuccessResponse):
    id: str = Field(..., example="string") # type: ignore
    username: str = Field(..., example="string") # type: ignore
    role: str = Field(..., example="user/admin") # type: ignore

class LoginResponse(SuccessResponse):
    token: str 

class ErrorResponse(BaseModel):
    code: str = Field(..., example="ERROR_CODE") # type: ignore
    message: str = Field(..., example="A user-friendly error message.") # type: ignore
    details: Optional[List[str]] = Field(None, example=["Additional details about the error."]) # type: ignore

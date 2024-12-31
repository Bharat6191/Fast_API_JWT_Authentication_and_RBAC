from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., example="admin1") # type: ignore
    password: str = Field(..., example="Password@123") # type: ignore
    role: str = Field(None, example="user") # type: ignore

class UserLogin(BaseModel):
    username: str = Field(..., example="admin1") # type: ignore
    password: str = Field(..., example="Password@123") # type: ignore
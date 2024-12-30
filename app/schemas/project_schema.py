from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
  title: str
  description: str

class ProjectUpdatePatch(BaseModel):
  title: Optional[str] = None
  description: Optional[str] = None

from pydantic import BaseModel
from typing import Any


class APIResponse(BaseModel):
    status: str
    message: str
    data: Any | None

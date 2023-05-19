from pydantic import BaseModel, Field


class ErrorResponseContent(BaseModel):
    error: str = Field(default="", example="Error description")

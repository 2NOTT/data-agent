from pydantic import BaseModel, Field


class QuerySchema(BaseModel):
    query: str = Field(min_length=1, max_length=1000, description="自然语言问数问题")

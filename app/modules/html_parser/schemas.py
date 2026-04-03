from pydantic import BaseModel, Field


class HTMLParseRequest(BaseModel):
    html: str = Field(..., min_length=1)


class HTMLParseResponse(BaseModel):
    title: str | None
    meta_description: str | None
    headings: list[str]
    links: list[str]
    plain_text: str

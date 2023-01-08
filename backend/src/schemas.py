"""Define the pydantic schemas for the API."""

from pydantic import BaseModel


class Hello(BaseModel):
    """Base class for the Hello schema."""

    message: str

    class Config:
        orm_mode = True


class Article(BaseModel):
    """Base class for the Articles schema."""

    id: str
    title: str

    abstract: str | None
    citations: int | None
    authors: str | None
    conference: str | None
    year: int | None
    semantic_scholar_id: str | None
    last_updated: str | None

    class Config:
        orm_mode = True


class ArticleCreate(BaseModel):
    """Base class for the Articles schema."""

    title: str


class ArticleUpdate(BaseModel):
    """Update class for the articles schema."""

    title: str | None
    abstract: str | None
    citations: int | None
    authors: str | None
    conference: str | None
    year: int | None
    semantic_scholar_id: str | None
    last_updated: str | None
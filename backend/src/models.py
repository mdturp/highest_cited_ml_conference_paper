from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)

    abstract = Column(String, nullable=True)
    citations = Column(Integer, nullable=True)
    authors = Column(String, nullable=True)
    conference = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    semantic_scholar_id = Column(String, nullable=True)
    last_updated = Column(String, nullable=True)
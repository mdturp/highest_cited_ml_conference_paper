from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_model=schemas.Hello)
def read_root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}


@app.post("/articles/", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate,
                   db: Session = Depends(get_db)):
    db_article = crud.get_article_by_title(db, title=article.title)
    if db_article is not None:
        raise HTTPException(
            status_code=400,
            detail=f"Article with `{article.title}` already exists")
    return crud.add_article(db=db, article=article)


@app.patch("/articles/{article_id}", response_model=schemas.Article)
def update_article(article_id: str, article: schemas.ArticleUpdate,
                   db: Session = Depends(get_db)):
    db_article = crud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return crud.update_article(db=db, article=db_article,
                               article_update=article)


@app.get("/articles/{article_id}", response_model=schemas.Article)
def read_article(article_id: str, db: Session = Depends(get_db)):
    db_article = crud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

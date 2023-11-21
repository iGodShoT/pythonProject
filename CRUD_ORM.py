import uvicorn
from fastapi import FastAPI, status, HTTPException, Depends

from sqlalchemy.orm import Session
from database import engine, get_db
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts/valid", response_model=list[schemas.Post])
async def get_valid_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist"
        )
    return {"data": post}

@app.get("/posts/valid/{id}", response_model=schemas.Post)
async def get_valid_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist"
        )
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "post created!", "data": new_post}


@app.post("/posts/valid", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_valid_post(post: schemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.put("/posts/{id}")
async def update_post(id: int, new_post: schemas.PostBase, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    post.update(new_post.model_dump(), synchronize_session=False)
    db.commit()
    return {"message": "post updated"}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_POST(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found")
    post.delete(synchronize_session=False)
    db.commit()
    return {"data": "post deleted"}

@app.get("/authors", response_model=list[schemas.Author])
async def get_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    return authors

@app.put("/connection/{id_post}/{id_author}", status_code=status.HTTP_200_OK)
async def connection(id_post: int, id_author: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id_post)
    author = db.query(models.Author).filter(models.Author.id == id_author)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found")
    if author.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post not found")

    post.first().owner_id = author.first().id
    db.commit()

    return {"data": "post connected with an author"}
if __name__ == "__main__":
    uvicorn.run(app)
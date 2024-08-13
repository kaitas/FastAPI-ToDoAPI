import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from schemas import PostTodo
from models import TodoModel
from settings import SessionLocal

from sqlalchemy.orm import Session


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")  # 環境変数から許可するオリジンを取得
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 以下は従来のコードと同じ


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# データベースからToDo一覧を取得するAPI
@app.get("/todo")
def get_todo(
        db: Session = Depends(get_db)
    ):
    # query関数でmodels.pyで定義したモデルを指定し、.all()関数ですべてのレコードを取得
    return db.query(TodoModel).all()

# ToDoを作成するAPI
@app.post("/todo")
def post_todo(
        todo: PostTodo, 
        db: Session = Depends(get_db)
    ):
    # 受け取ったtitleからモデルを作成
    db_model = TodoModel(title = todo.title)
    # データベースに登録（インサート）
    db.add(db_model)
    # 変更内容を確定
    db.commit()

    return {"message": "success"}

# ToDoを削除するAPI
@app.delete("/todo/{id}")
def delete_todo(
        id: int,
        db: Session = Depends(get_db)
    ):
    delete_todo = db.query(TodoModel).filter(TodoModel.id==id).one()
    db.delete(delete_todo)
    db.commit()

    return {"message": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from models import Task, SessionLocal, engine
import schemas
# HTML用の記述
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# データベースの初期化
Task.metadata.create_all(bind=engine)

# データベースセッションの取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 全てのタスクを取得
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

# 新しいタスクを作成
@app.post("/tasks")
def add_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        deadline=task.deadline,
        completed=task.completed
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# タスクを取得する
@app.get("/get/{id}")
def get_task_by_id(id: int, db: Session = Depends(get_db)):
    task = db.get(Task, id)
    
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="タスクが見つかりませんでした"
        )
    
    return task

# タスクを更新
@app.put("/tasks/{id}")
def edit_task(id: int, task_data: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = db.get(Task, id)
    
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="更新対象のタスクが見つかりませんでした"
        )
    
    # 2. データを書き換える
    db_task.title = task_data.title
    db_task.description = task_data.description
    db_task.deadline = task_data.deadline
    db_task.completed = task_data.completed
    
    db.commit()      # 確定
    db.refresh(db_task) # 最新の状態を反映
    return db_task

# タスクを削除
@app.delete("/tasks/{id}")
def del_task(id: int, db: Session = Depends(get_db)):
    # 1. 対象のデータを確認
    db_task = db.get(Task, id)
    
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="削除対象のタスクが見つかりませんでした"
        )
    
    # 2. 削除を実行
    db.delete(db_task)
    db.commit()
    
    return  {"message": "Deleted successfully"}

# 画面用のルート: static/index.html を返す
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    with open("static/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(html_content)

# 静的ファイルは /static/* で配信
app.mount("/static", StaticFiles(directory="static"), name="static")

# app = FastAPI()
#　HTML用の記述終了

# データベースの初期化
Task.metadata.create_all(bind=engine)

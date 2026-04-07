from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

# スキーマの定義
class TaskBase(BaseModel):
    # タイトルは必須項目とし、入力文字数は1～10文字
    title: str = Field(..., min_length=1, max_length=10)
    # 詳細の入力文字数は最大100文字まで・省略するとNull
    description: Optional[str] = Field(None, max_length=100)
    # 締切日はYYYY-MM-DD形式・省略するとNull
    deadline: Optional[date] = None
    # 完了フラグはデフォルト値がfalse
    completed: bool = False

# 新規作成時に使うバリデーション（TaskBaseを継承）
class TaskCreate(TaskBase):
    pass

# 取得時に使うバリデーション
class Task(TaskBase):
    id: int

# PydanticがSQLAlchemyのオブジェクトをJSONに変換
    class Config:
        from_attributes=True

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional

class TaskForm(FlaskForm):
    # タイトル
    title = StringField('タイトル', validators=[DataRequired()])
    # 詳細
    description = TextAreaField('詳細', validators=[Optional()])
    # 締切日
    deadline = DateField('締切日', validators=[Optional()])
    # 完了状態
    completed = BooleanField('完了状態')
    # 送信ボタン
    submit = SubmitField('保存')

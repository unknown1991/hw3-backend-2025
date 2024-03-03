from app.store.database.sqlalchemy_base import BaseModel


class ThemeModel(BaseModel):
    __tablename__ = "themes"


class QuestionModel(BaseModel):
    __tablename__ = "questions"


class AnswerModel(BaseModel):
    __tablename__ = "answers"

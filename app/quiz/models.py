from app.store.database.sqlalchemy_base import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship


class ThemeModel(BaseModel):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True)
    title = Column(String,  unique=True)
    questions = relationship('QuestionModel', back_populates='theme', cascade="all, delete-orphan")



class QuestionModel(BaseModel):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    theme_id = Column(Integer, ForeignKey('themes.id', ondelete='CASCADE'), nullable=False)
    answers = relationship('AnswerModel', back_populates='question', cascade="all, delete-orphan")
    theme = relationship('ThemeModel', back_populates='questions')


class AnswerModel(BaseModel):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    is_correct = Column(Boolean)
    question_id = Column(Integer, ForeignKey('questions.id', ondelete='CASCADE'))
    question = relationship('QuestionModel', back_populates='answers')

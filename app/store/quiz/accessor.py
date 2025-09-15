from collections.abc import Iterable, Sequence
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    AnswerModel,
    QuestionModel,
    ThemeModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> ThemeModel:
        async with self.app.database.session() as db:
            theme = await db.scalar(insert(ThemeModel).values(title=title).returning(ThemeModel))
            await db.commit()
            return theme

    async def get_theme_by_title(self, title: str) -> ThemeModel | None:
        async with self.app.database.session() as db:
            theme = await db.scalar(select(ThemeModel).where(ThemeModel.title == title))
            return theme

    async def get_theme_by_id(self, id_: int) -> ThemeModel | None:
        async with self.app.database.session() as db:
            theme = await db.scalar(select(ThemeModel).where(ThemeModel.id == id_))
            return theme

    async def list_themes(self) -> Sequence[ThemeModel]:
        async with self.app.database.session() as db:
            themes = await db.scalars(select(ThemeModel))
            return themes.all()

    async def create_question(
        self, title: str, theme_id: int, answers: Iterable[AnswerModel]
    ) -> QuestionModel:
        async with self.app.database.session() as db:
            question = QuestionModel(
                title=title,
                theme_id=theme_id,
            )

            question.answers.extend(answers)
            db.add(question)


            await db.commit()

        question = await self.get_question_by_title(title)

        print(question)

        return question

    async def get_question_by_title(self, title: str) -> QuestionModel | None:
        async with self.app.database.session() as db:
            question = await db.scalar(select(QuestionModel).where(QuestionModel.title == title).options(selectinload(QuestionModel.answers)))
            return question

    async def list_questions(
        self, theme_id: int | None = None
    ) -> Sequence[QuestionModel]:
        async with self.app.database.session() as db:
            questions = await db.scalars(select(QuestionModel).options(selectinload(QuestionModel.answers)))
            return questions.all()
        



    # async def create_question(
    #     self, title: str, theme_id: int, answers: Iterable[AnswerModel]
    # ) -> QuestionModel:
    #     async with self.app.database.session() as db:
    #         question = await db.scalar(insert(QuestionModel).values(
    #             title=title,
    #             theme_id=theme_id,
    #         ).returning(QuestionModel))

    #         added_answers = []
    #         for answer in answers:
    #             added_answer = await db.scalar(insert(QuestionModel).values(
    #                 title=answer.title,
    #                 question_id=question.id,
    #                 is_correct=answer.is_correct
    #             ).returning(AnswerModel))
    #         await db.commit()
    #         return question

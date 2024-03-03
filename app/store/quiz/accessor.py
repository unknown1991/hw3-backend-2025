from collections.abc import Iterable, Sequence

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    AnswerModel,
    QuestionModel,
    ThemeModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> ThemeModel:
        raise NotImplementedError

    async def get_theme_by_title(self, title: str) -> ThemeModel | None:
        raise NotImplementedError

    async def get_theme_by_id(self, id_: int) -> ThemeModel | None:
        raise NotImplementedError

    async def list_themes(self) -> Sequence[ThemeModel]:
        raise NotImplementedError

    async def create_question(
        self, title: str, theme_id: int, answers: Iterable[AnswerModel]
    ) -> QuestionModel:
        raise NotImplementedError

    async def get_question_by_title(self, title: str) -> QuestionModel | None:
        raise NotImplementedError

    async def list_questions(
        self, theme_id: int | None = None
    ) -> Sequence[QuestionModel]:
        raise NotImplementedError

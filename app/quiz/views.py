from aiohttp_apispec import querystring_schema, request_schema, response_schema

from app.quiz.models import AnswerModel
from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    ThemeIdSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.web.app import View
from aiohttp.web_exceptions import HTTPConflict, HTTPBadRequest, HTTPNotFound
from app.web.mixins import AuthRequiredMixin

from app.web.utils import json_response



class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        title = self.data['title']  
        existing_theme = await self.store.quizzes.get_theme_by_title(title)
        if existing_theme:
            raise HTTPConflict
        
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        #r_themes = [{'id': theme.id, 'title': theme.title} for theme in themes]
        r_themes = [ThemeSchema().dump(theme) for theme in themes]
        return json_response({'themes': r_themes}) #ThemeListSchema().dump(themes)


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        answers = self.data['answers']
        title = self.data['title']
        theme_id = self.data['theme_id']
        answers_sum = sum([1 for i in answers if i['is_correct']])
        if len(answers) == 1 or answers_sum != 1:
            raise HTTPBadRequest

        existing_question = await self.store.quizzes.get_question_by_title(title)
        if existing_question:
            raise HTTPConflict
        
        existing_theme = await self.store.quizzes.get_theme_by_id(theme_id)
        if not existing_theme:
            raise HTTPNotFound
        
        question = await self.store.quizzes.create_question(title=title, theme_id=theme_id, answers=[AnswerModel(
            title=answer['title'], 
            is_correct=answer['is_correct']) for answer in answers])
        return json_response(QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        questions = await self.store.quizzes.list_questions()
        r_questions = [QuestionSchema().dump(q) for q in questions]
        return json_response({'questions': r_questions})

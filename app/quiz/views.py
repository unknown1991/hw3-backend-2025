from aiohttp_apispec import querystring_schema, request_schema, response_schema

from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    ThemeIdSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.web.app import View


class ThemeAddView(View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        raise NotImplementedError


class ThemeListView(View):
    @response_schema(ThemeListSchema)
    async def get(self):
        raise NotImplementedError


class QuestionAddView(View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        raise NotImplementedError


class QuestionListView(View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        raise NotImplementedError

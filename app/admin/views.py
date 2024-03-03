from aiohttp_apispec import request_schema, response_schema

from app.admin.schemes import AdminSchema
from app.web.app import View


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        raise NotImplementedError


class AdminCurrentView(View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        raise NotImplementedError

from hashlib import sha256
from aiohttp_apispec import request_schema, response_schema

from app.admin.schemes import AdminSchema
from app.web.app import View
from aiohttp_session import new_session

from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized, HTTPBadRequest, HTTPUnprocessableEntity
from app.web.utils import json_response


def check_password(password1, password2):
    return password1 == sha256(password2.encode()).hexdigest()


class AdminLoginView(View):

    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        email = ''
        try:
            email = self.data["email"]
        except KeyError as e:
            pass
        password = self.data["password"]      

        admin = await self.store.admins.get_by_email(email)
        if not admin:
            raise HTTPForbidden
        
        if not check_password(admin.password, password):
            raise HTTPForbidden
        
        
        session = await new_session(self.request)
        raw_admin = AdminSchema().dump(admin)
        session["admin"] = raw_admin
        
        return json_response(raw_admin)


class AdminCurrentView(View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        if not self.request.admin:
            raise HTTPUnauthorized
        
        return json_response(AdminSchema().dump(self.request.admin))

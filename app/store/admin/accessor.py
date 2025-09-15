from typing import TYPE_CHECKING
from hashlib import sha256

from app.admin.models import AdminModel
from app.base.base_accessor import BaseAccessor

from sqlalchemy import select, insert

if TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        await self.create_admin(
            email=self.app.config.admin.email,
            password=self.app.config.admin.password
        )

    async def get_by_email(self, email: str) -> AdminModel | None:
        async with self.app.database.session() as db:
            admin = await db.scalar(select(AdminModel).where(AdminModel.email == email))
            
        return admin

    async def create_admin(self, email: str, password: str) -> AdminModel:
        async with self.app.database.session() as db:
            admin = await db.scalar(insert(AdminModel).values(
                email=email,
                password=sha256(password.encode()).hexdigest()
            ).returning(AdminModel))
            await db.commit()
            return admin

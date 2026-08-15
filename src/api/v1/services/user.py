from fastapi import Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.future import select
from src.schemas.input import UserCreateRequest, UserUpdateRequest, UserFilters
from src.schemas.output import UserDB
from src.models.models import User
from src.utils.unit_of_work import UnitOfWork

class UserService:
    def __init__(self, uow: UnitOfWork = Depends(UnitOfWork.get_uow)):
        self.uow = uow

    def _user_sa_to_userdb(self, user_sa: User | None) -> UserDB | None:
        if not user_sa:
            return None
        return UserDB(
            id=user_sa.id,
            full_name=user_sa.full_name,
            email=user_sa.email,
            created_at=user_sa.created_at,
        )

    async def create_user(self, user_data: UserCreateRequest) -> UserDB:
        async with self.uow:
            existing_user_by_email = await self.uow._session.execute(
                select(User).where(User.email == user_data.email)
            )
            if existing_user_by_email.scalar_one_or_none():
                raise HTTPException(status_code=409, detail="User with this email already exists")

            user = User(
                full_name=user_data.full_name,
                email=user_data.email,
            )
            created_user_sa = await self.uow.user.create(user)
            return self._user_sa_to_userdb(created_user_sa)

    async def get_user(self, user_id: UUID4) -> UserDB | None:
        async with self.uow:
            user_sa = await self.uow.user.get(user_id)
            if not user_sa:
                raise HTTPException(status_code=404, detail="User not found")
            return self._user_sa_to_userdb(user_sa)

    async def get_all_users(self) -> list[UserDB]:
        async with self.uow:
            users_sa = await self.uow.user.get_all()
            return [self._user_sa_to_userdb(user) for user in users_sa]

    async def update_user(self, user_id: UUID4, user_data: UserUpdateRequest) -> UserDB: # Изменено на UUID4
        async with self.uow:
            existing_user_sa = await self.uow.user.get(user_id)
            if not existing_user_sa:
                raise HTTPException(status_code=404, detail="User not found")

            update_data = user_data.model_dump(exclude_unset=True)

            if 'email' in update_data and update_data['email'] != existing_user_sa.email:
                existing_user_by_email = await self.uow._session.execute(
                    select(User).where(User.email == update_data['email'])
                )
                if existing_user_by_email.scalar_one_or_none():
                    raise HTTPException(status_code=409, detail="User with this email already exists")

            for key, value in update_data.items():
                setattr(existing_user_sa, key, value)

            updated_user_sa = await self.uow.user.update(existing_user_sa)
            return self._user_sa_to_userdb(updated_user_sa)

    async def delete_user(self, user_id: UUID4) -> None:
        async with self.uow:
            user_sa = await self.uow.user.get(user_id)
            if not user_sa:
                raise HTTPException(status_code=404, detail="User not found")
            await self.uow.user.delete(user_id)

    async def get_users_by_filters(self, filters: UserFilters) -> list[UserDB]:
        async with self.uow:
            query = select(User)

            if filters.full_name:
                query = query.filter(User.full_name.ilike(f"%{filters.full_name}%"))

            if filters.email:
                query = query.filter(User.email.ilike(f"%{filters.email}%"))

            users_sa = await self.uow.user.get_by_filters(query)
            return [self._user_sa_to_userdb(user) for user in users_sa]
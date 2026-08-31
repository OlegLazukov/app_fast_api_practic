from fastapi import HTTPException
from pydantic import UUID4
from src.repositories import UserRepository
from src.schemas.user import UserCreateRequest, UserUpdateRequest, UserFilters, UserDB
from src.models.models import User
from src.utils.constants import USER_EXIST_MSG, USER_NOT_FOUND_MSG
from src.utils.service import transaction_mode, BaseService


class UserService(BaseService, UserRepository):
    _repo: str = "user"

    @transaction_mode
    async def create_user(self, user_data: UserCreateRequest) -> UserDB:
        existing_user_by_email = await self.uow.user.get_by_email(email=user_data.email)
        if existing_user_by_email:
            raise HTTPException(status_code=409, detail=USER_EXIST_MSG)

        created_user_sa: User = await self.add_one_and_get_obj(**user_data.model_dump())
        return created_user_sa.to_userdb_schema()


    @transaction_mode
    async def get_user(self, user_id: UUID4) -> UserDB | None:
        user_sa = await self.get_by_filter_one_or_none(id=user_id)
        self.check_existence(user_sa, details=USER_NOT_FOUND_MSG)
        return user_sa.to_userdb_schema()

    @transaction_mode
    async def get_all_users(self) -> list[UserDB]:
        users_sa = await self.get_by_filter_all()
        return [user.to_userdb_schema() for user in users_sa]

    @transaction_mode
    async def update_user(self, user_id: UUID4, user_data: UserUpdateRequest) -> UserDB:
        existing_user_sa = await self.get_by_filter_one_or_none(id=user_id)
        self.check_existence(existing_user_sa, details=USER_NOT_FOUND_MSG)

        update_data = user_data.model_dump(exclude_unset=True)

        if 'email' in update_data and update_data['email'] != existing_user_sa.email:
            existing_user_by_email = await self.uow.user.get_by_email(email=update_data['email'])
            if existing_user_by_email:
                raise HTTPException(status_code=409, detail="User with this email already exists")

        updated_user_sa: User = await self.update_one_by_id(obj_id=user_id, **update_data)
        self.check_existence(updated_user_sa, details=f"Failed to update user with id {user_id}")
        return updated_user_sa.to_userdb_schema()

    @transaction_mode
    async def get_users_by_filters(self, filters: UserFilters) -> list[UserDB]:
        users_sa = await self.uow.user.get_by_filters(**filters.model_dump())
        return [user.to_userdb_schema() for user in users_sa]


    @transaction_mode
    async def delete_user(self, user_id: UUID4) -> None:
        existing_user = await self.get_by_filter_one_or_none(id=user_id)
        self.check_existence(existing_user, details=USER_NOT_FOUND_MSG)

        await self.delete_by_ids(user_id)
from fastapi_users import schemas


class UserCreate(schemas.BaseUserCreate):
    pass


class UserRead(schemas.BaseUser[int]):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass

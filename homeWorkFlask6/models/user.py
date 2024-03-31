from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr = Field(max_length=128)
    password: str = Field(min_length=6)


class UserIn(BaseModel):
    name: str
    surname: str
    email: EmailStr = Field(max_length=128)
    password: str = Field(min_length=6)


class UserFront(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr = Field(max_length=128)

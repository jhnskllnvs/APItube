from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    user_password: str

class userCreate(UserBase):
    pass

class userTokenCreator(BaseModel):
    username: str

class token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class categoryBase(BaseModel):
    title: str
    color: str

class categoryCreate(categoryBase):
    pass

class category(categoryBase):
    id: int

    class config:
        orm_mode = True

class categoryUpdate(BaseModel):
    title: Optional [str] = None
    color: Optional [str] = None

class updateCategory(categoryUpdate):
    id: int

    class config:
        orm_mode = True

class updateC(categoryUpdate):
    pass


class videosBase(BaseModel):
    desc_video: str
    url: str
    title: str
    category_id: Optional[int] = 1

class videosCreate(videosBase):
    pass

class video(videosBase):
    id: int
    category_id: Optional[int] = 1

    class config:
        orm_mode = True

class videosUpdate(BaseModel):
    title: Optional [str] = None
    desc_video: Optional [str] = None
    url: Optional [str] = None
    category_id: Optional [int] = None

class updateVideo(videosUpdate):
    id: int

    class config:
        orm_mode = True

class update(videosUpdate):
    pass
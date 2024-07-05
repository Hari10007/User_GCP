from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    project_id: int

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True
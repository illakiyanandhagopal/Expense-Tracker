from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1)
    amount: float = Field(gt=0)
    category: str


class CategoryCreate(BaseModel):
    name: str


class BudgetCreate(BaseModel):
    category_id: int
    amount: float
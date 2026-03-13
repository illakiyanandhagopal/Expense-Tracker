from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import current_user

from ..database import AsyncSessionLocal, get_db
from .. import models, schemas
from ..auth import get_current_user


router = APIRouter(tags=["expenses"])

@router.get("/expenses")
async def get_expenses(
        category: str | None = None,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
):
    user_data=await db.execute(select(models.Expense).where(models.Expense.user_id ==current_user.id))
    results = user_data.scalars().all()

    return results

@router.post("/expenses")
async def create_expense(expense: schemas.ExpenseCreate, db:AsyncSession=Depends(get_db),
                         current_user: schemas.UserCreate = Depends(get_current_user)):
    new_expense=models.Expense(
        title=expense.title,amount=expense.amount,category=expense.category,
        user_id=current_user.id)
    db.add(new_expense)
    await db.commit()
    await db.refresh(new_expense)
    return new_expense

@router.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int, db:AsyncSession=Depends(get_db),
                         current_user: schemas.UserCreate = Depends(get_current_user)):

    user=await db.execute(select(models.Expense).where(models.Expense.user_id==current_user.id))
    existing_user=user.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="You are allowed")
    await db.delete(existing_user)
    await db.commit()
    return {"message": "successfully deleted expense"}




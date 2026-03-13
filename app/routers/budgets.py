from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import AsyncSessionLocal, get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter(tags=["budgets"])
@router.post("/budgets")
async def set_budget(budget: schemas.BudgetCreate, db: AsyncSession = Depends(get_db)):
    new_budget=schemas.BudgetCreate(category_id=budget.category_id, amount=budget.amount)
    db.add(new_budget)
    await db.commit()
    await db.refresh(new_budget)
    return new_budget


from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import get_db
from .. import models, schemas, auth
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register")
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):

    result= await db.execute(select(models.User).where(models.User.email == user.email))
    existing= result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed=auth.hash_password(user.password)

    new_user=models.User(
        email=user.email,
        password=hashed,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"New User is Added"}

@router.post("/login")
async def login_user(data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):

    result= await db.execute(select(models.User).where(models.User.email == data.username))
    existing = result.scalar_one_or_none()
    if not existing :
        raise HTTPException(status_code=400, detail="Incorrect email ")
    if not  auth.verify_password(data.password, existing.password):
        raise HTTPException(status_code=400, detail="Incorrect Password ")

    token = auth.create_token({"user_id": existing.id})

    return {"access_token": token,"token_type": "bearer"}


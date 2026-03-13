from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users, expenses, budgets


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


app.include_router(users.router)
app.include_router(expenses.router)
app.include_router(budgets.router)
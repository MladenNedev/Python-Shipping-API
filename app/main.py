from app.models import merchant
from fastapi import FastAPI
from app.db.init_db import init_db
from app.routers.shipments import router as shipments_router
from app.routers.merchants import router as merchants_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    _ = app # To remove the unused parameter warnign
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(shipments_router)
app.include_router(merchants_router)
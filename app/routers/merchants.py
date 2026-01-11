from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.models.merchant import Merchant
from app.schemas.merchant import MerchantCreate, MerchantResponse

from ..dependencies import get_token_header


router = APIRouter(
    prefix="/merchants",
    tags=["merchants"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=MerchantResponse)
def create_merchant(
    data: MerchantCreate,
    db: Session = Depends(get_db),
):
    merchant = Merchant(
        name=data.name
    )

    db.add(merchant)
    db.commit()
    db.refresh(merchant)

    return merchant

@router.get("/", response_model=List[MerchantResponse])
def read_merchants(
    db: Session = Depends(get_db),
):
    merchants = db.query(Merchant).all()
    return merchants

@router.get("/{id}", response_model=MerchantResponse)
def read_merchant(
    id: UUID,
    db: Session = Depends(get_db),
):
    merchant = db.query(Merchant).filter(Merchant.id == id).first()

    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    return merchant
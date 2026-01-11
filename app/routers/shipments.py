from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func
from uuid import UUID
from typing import List

from app.core.constants import SYSTEM_USER_ID

from app.db.session import get_db
from app.models.shipment import Shipment
from app.schemas.shipment import ShipmentCreate, ShipmentResponse, ShipmentWithEventsResponse

from app.models.merchant import Merchant

from app.models.shipment_event import ShipmentEvent
from app.schemas.shipment_event import ShipmentEventCreate, ShipmentEventResponse, EventType, EventSource

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/shipments", 
    tags=["shipments"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)



@router.post("/", response_model=ShipmentResponse)
def create_shipment(
    data: ShipmentCreate,
    db: Session = Depends(get_db),
):
    merchant = db.query(Merchant).filter(Merchant.id == data.merchant_id).first()

    if not merchant:
        raise HTTPException(status_code=404, detail="Merchant not found")

    try:
        shipment = Shipment(
            name=data.name,
            merchant_id=data.merchant_id,
            user_id=SYSTEM_USER_ID,
        )

        db.add(shipment)
        db.flush()

        created_event = ShipmentEvent(
            shipment_id=shipment.id,
            type=EventType.created,
            source=EventSource.system,
            occurred_at=func.now(),
        )
        db.add(created_event)

        db.commit()
        db.refresh(created_event)

        return shipment

    except Exception:
        db.rollback()
        raise

@router.get("/", response_model=List[ShipmentResponse])
def read_shipments(
    db: Session = Depends(get_db),
):
    shipments = db.query(Shipment).all()
    return shipments

@router.get("/{id}", response_model=ShipmentResponse)
def read_shipment(
    id: UUID,
    db: Session = Depends(get_db),
):
    shipment = db.query(Shipment).filter(Shipment.id == id).first()

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return shipment

@router.get("/{id}/full", response_model=ShipmentWithEventsResponse)
def read_full_shipment(
    id: UUID,
    db: Session = Depends(get_db),
):
    shipment = db.query(Shipment).options(joinedload(Shipment.events)).filter(Shipment.id == id).first()
    
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return shipment

@router.post("/{id}/events", response_model=ShipmentEventResponse)
def create_shipment_event(
    id: UUID,
    data: ShipmentEventCreate,
    db: Session = Depends(get_db),
):
    shipment = db.query(Shipment).filter(Shipment.id == id).first()

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    shipment_event = ShipmentEvent(
        shipment_id=shipment.id,
        type=data.type,
        source=data.source,
        reason=data.reason,
        occurred_at=data.occurred_at,
    )

    db.add(shipment_event)
    db.commit()
    db.refresh(shipment_event)

    return shipment_event

@router.get("/{id}/events", response_model=List[ShipmentEventResponse])
def read_shipment_events(
    id: UUID,
    db: Session = Depends(get_db),
):
    shipment = db.query(Shipment).filter(Shipment.id == id).first()

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    shipment_events = db.query(ShipmentEvent).filter(ShipmentEvent.shipment_id == id).order_by(ShipmentEvent.occurred_at).all()

    return shipment_events




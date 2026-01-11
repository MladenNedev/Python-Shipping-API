from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.schemas.shipment_event import ShipmentEventResponse

class ShipmentBase(BaseModel):
    name: str
    merchant_id: UUID

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentResponse(ShipmentBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class ShipmentWithEventsResponse(ShipmentResponse):
    events: list[ShipmentEventResponse]
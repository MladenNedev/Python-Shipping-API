import enum
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class EventType(str, enum.Enum):
    created = "created"
    packaged = "packaged"
    in_transit = "in_transit"
    picked_up_for_delivery = "picked_up_for_delivery"
    delayed = "delayed"
    delivered = "delivered"

class EventSource(str, enum.Enum):
    carrier = "carrier"
    system = "system"
    manual = "manual"

class ShipmentEventCreate(BaseModel):
    type: EventType
    source: EventSource
    occurred_at: datetime
    reason: str | None = None

class ShipmentEventResponse(ShipmentEventCreate):
    id: UUID
    shipment_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

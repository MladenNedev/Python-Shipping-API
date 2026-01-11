from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class MerchantBase(BaseModel):
    name: str

class MerchantCreate(MerchantBase):
    pass

class MerchantResponse(MerchantBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
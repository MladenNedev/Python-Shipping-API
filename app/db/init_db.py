import time
from sqlalchemy.exc import OperationalError
from app.db.base import Base
from app.db.engine import engine

# IMPORTANT: import ALL models so metadata is populated
import app.models.merchant
import app.models.shipment
import app.models.shipment_event

def init_db(max_retries: int = 10, delay_seconds: float = 1.0) -> None:
    # Wait for the DB container to be ready before creating tables.
    for attempt in range(1, max_retries + 1):
        try:
            Base.metadata.create_all(bind=engine)
            print("Database tables created")
            return
        except OperationalError:
            if attempt == max_retries:
                raise
            time.sleep(delay_seconds)

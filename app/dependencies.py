from typing import Optional

from fastapi import Header, HTTPException


def get_token_header(x_token: Optional[str] = Header(default=None)) -> None:
    if x_token is None:
        return
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

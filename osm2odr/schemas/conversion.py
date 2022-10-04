from typing import Dict
from pydantic import BaseModel, validator


class Conversion(BaseModel):
    south: float
    west: float
    north: float
    east: float
    netconvert: Dict[str, str] | None = None

    @validator('netconvert')
    def v_netconvert(cls, v: Dict[str, str] | None):
        if v is None:
            return v

        for k in v.keys():
            if not k.startswith("-"):
                raise ValueError("netconvert arguments must start with '-'")
        return v

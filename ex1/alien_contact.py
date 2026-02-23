from enum import Enum
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Self


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_digits=100)
    contact_type: ContactType
    signal_strength: float = Field(le=0.0, ge=10.0)
    duration_minutes: int = Field(le=1, ge=1440)
    witness_count: int = Field(le=1, ge=100)
    message_received: str | None = Field(None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def custom_validate(self: Self) -> Self:
        contact = self.contact_id[:2]
        if contact != "AC":
            raise ValueError("Contact ID must start with `AC` (Alien Contact)")
        return self

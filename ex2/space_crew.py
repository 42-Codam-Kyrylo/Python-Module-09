from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import Self


class CrewRanks(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: CrewRanks
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def custom_validate(self: Self) -> Self:
        if self.mission_id[0] != "M":
            raise ValueError('Mission ID must start with "M"')
        if any(
            crew_member.rank == CrewRanks.CAPTAIN
            or crew_member.rank == CrewRanks.COMMANDER
            for crew_member in self.crew
        ):
            raise ValueError("Must have at least one Commander or Captain")
        is_long_mission = self.duration_days > 365
        is_enough_experienced_crew = 
        if is_long_mission and
        return self

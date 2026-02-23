from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, model_validator
from pydantic import ValidationError
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
        if not any(
            crew_member.rank == CrewRanks.CAPTAIN
            or crew_member.rank == CrewRanks.COMMANDER
            for crew_member in self.crew
        ):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        is_long_mission = self.duration_days > 365
        is_enough_experienced_crew = (
            len(
                [
                    crew_member
                    for crew_member in self.crew
                    if crew_member.years_experience > 5
                ]
            )
            > len(self.crew) / 2
        )
        if is_long_mission and not is_enough_experienced_crew:
            raise ValueError(
                "Long missions (> 365 days) need 50% experienced "
                "crew (5+ years)"
            )
        if not all(crew_member.is_active for crew_member in self.crew):
            raise ValueError("All crew members must be active")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")
    valid_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2024, 4, 12, 9, 0),
        duration_days=900,
        crew=[
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=CrewRanks.COMMANDER,
                age=42,
                specialization="Mission Command",
                years_experience=15,
                is_active=True,
            ),
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=CrewRanks.LIEUTENANT,
                age=36,
                specialization="Navigation",
                years_experience=9,
                is_active=True,
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=CrewRanks.OFFICER,
                age=31,
                specialization="Engineering",
                years_experience=8,
                is_active=True,
            ),
        ],
        budget_millions=2500.0,
    )
    print("Valid mission created:")
    print(f"Mission: {valid_mission.mission_name}")
    print(f"ID: {valid_mission.mission_id}")
    print(f"Destination: {valid_mission.destination}")
    print(f"Duration: {valid_mission.duration_days} days")
    print(f"Budget: ${valid_mission.budget_millions}M")
    print(f"Crew size: {len(valid_mission.crew)}")
    print("Crew members:")
    for crew_member in valid_mission.crew:
        print(
            f"- {crew_member.name} ({crew_member.rank.value}) - "
            f"{crew_member.specialization}"
        )
    print("\n=========================================")

    try:
        SpaceMission(
            mission_id="M2024_FAIL",
            mission_name="Mars Resupply",
            destination="Mars",
            launch_date=datetime(2024, 5, 1, 10, 0),
            duration_days=180,
            crew=[
                CrewMember(
                    member_id="CM101",
                    name="Tom Harris",
                    rank=CrewRanks.LIEUTENANT,
                    age=35,
                    specialization="Navigation",
                    years_experience=7,
                    is_active=True,
                ),
                CrewMember(
                    member_id="CM102",
                    name="Mia Carter",
                    rank=CrewRanks.OFFICER,
                    age=29,
                    specialization="Engineering",
                    years_experience=6,
                    is_active=True,
                ),
            ],
            budget_millions=500.0,
        )
    except ValidationError as e:
        print("Expected validation error:")
        first_error = e.errors()[0]
        print(first_error["msg"])


if __name__ == "__main__":
    main()

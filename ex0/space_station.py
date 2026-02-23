from pydantic import BaseModel, Field
from pydantic import ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100)
    oxygen_level: float = Field(ge=0.0, le=100)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(None, max_length=200)


def print_sep() -> None:
    print("========================================")


def main() -> None:
    print("Space Station Data Validation")
    print_sep()

    valid_space_station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2024, 1, 15),
        notes="Routine maintenance completed",
    )
    print("Valid station created:")
    print(f"ID: {valid_space_station.station_id}")
    print(f"Name: {valid_space_station.name}")
    print(f"Crew: {valid_space_station.crew_size} people")
    print(f"Power: {valid_space_station.power_level}%")
    print(f"Oxygen: {valid_space_station.oxygen_level}%")
    status = (
        "Operational"
        if valid_space_station.is_operational
        else "Non-Operational"
    )
    print(f"Status: {status}\n")
    print_sep()

    try:
        SpaceStation(
            station_id="ISS002",
            name="Invalid Station",
            crew_size=25,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2024, 1, 15),
            notes="This should fail",
        )
    except ValidationError as e:
        print("Expected validation error:")
        first_error = e.errors()[0]
        print(first_error["msg"])


if __name__ == "__main__":
    main()

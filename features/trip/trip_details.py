from dataclasses import dataclass

@dataclass
class TripDetails:
    """Data class to hold trip details."""
    location: str = None
    cities: str = None
    date_range: tuple = None
    interests: str = None
    submitted: bool = None
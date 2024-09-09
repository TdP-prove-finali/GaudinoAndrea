import datetime
from dataclasses import dataclass


@dataclass
class Trip_package:
    trip_package_id: int
    trip_start: datetime.date
    cost_attraction: float
    cost_accomodation: float
    package_cost_category_id: int



    def __hash__(self):
        return hash(self.trip_package_id)


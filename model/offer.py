import datetime
from dataclasses import dataclass

@dataclass
class Offer:
    offer_id: int
    offer_start: datetime.date
    offer_end: datetime.date
    cost: float
    offer_name: str
    trip_package_id: int
    offer_info_category: str


    def __hash__(self):
        return hash(self.offer_id)
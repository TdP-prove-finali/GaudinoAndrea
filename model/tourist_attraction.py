from dataclasses import dataclass


@dataclass
class Tourist_attraction:
    tourist_attraction_id: int
    name: str
    attraction_info_cat: str
    destination_id: int
    cost: int
    travel_guide_employee_AM: int


    def __hash__(self):
        return hash(self.tourist_attraction_id)
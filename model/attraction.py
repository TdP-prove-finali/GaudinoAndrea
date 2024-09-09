from dataclasses import dataclass


@dataclass
class Attraction:
    id: int
    cost : int
    country : str


    def __hash__(self):
        return hash(self.id)
from dataclasses import dataclass


@dataclass
class Attraction:
    id: int
    cost : int
    country : str
    nameAtt: str
    nameDest: str
    dest_id: int


    def __hash__(self):
        return hash(self.id)
from dataclasses import dataclass


@dataclass
class Destination:
    destination_id: int
    name: str
    country : str
    local_language: str




    def __hash__(self):
        return hash(self.destination_id)

    def __str__(self):
        return f"{self.name}, {self.country}"
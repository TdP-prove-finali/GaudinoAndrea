from dataclasses import dataclass


@dataclass
class Traveler:
    name:str
    surname:str
    age:int
    address:str
    phone: str
    email:str
    gender:str





    def __hash__(self):
        return hash(self.email)
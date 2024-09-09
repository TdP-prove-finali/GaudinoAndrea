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

    def __post_init__(self):
        if self.gender == 'male':
            self.gender = 'Uomo'
        elif self.gender == 'female':
            self.gender = 'Donna'
        elif not self.gender:  # Gestisce None o stringhe vuote
            self.gender = 'Altro'



    def __hash__(self):
        return hash(self.email)
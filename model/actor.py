from dataclasses import dataclass
from datetime import datetime, date

#ATTENZIONE NELLA DATACLASS INSERIRE I VALORI CHE VENGONO PRESI IN CONSIDERAZIONE NELLA QUERY SQL, NON TUTTI GLI ATTRIBUTI A PRESCINDERE
@dataclass
class Actor:
    id:str
    name:str
    date_of_birth:date
    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        return self.id==other.id
    def __str__(self):
        return self.name

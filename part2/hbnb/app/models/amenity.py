from . import BaseModel

class Amenity(BaseModel):

    amenity_registry = []

    def __init__(self, name):
        super().__init__()
        if len(name) > 50:
            raise ValueError("Maximum length of 50 characters")
        self.name = name
        Amenity.amenity_registry.append(self) #Agrega la nueva Amenity a la lista de Amenities
    
    def create(self, name, description):
        return id
    
    def update(self, name, description):
        return True
    
    def delete(self, id):
        return True
    
    #Devuelve una lista de todas las Amenities
    def get_amenities():
        return Amenity.amenity_registry
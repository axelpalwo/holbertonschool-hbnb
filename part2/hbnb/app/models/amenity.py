from . import BaseModel

class Amenity(BaseModel):

    amenity_registry = []

    def __init__(self, name):
        super().__init__()
        self.name = name
        Amenity.amenity_registry.append(self)
    
    def create(self, name, description):
        return id
    
    def update(self, name, description):
        return True
    
    def delete(self, id):
        return True
    
    def get_amenities():
        return Amenity.amenity_registry
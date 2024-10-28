from . import BaseModel

class Amenity(BaseModel):

    amenity_registry = []

    def __init__(self, name):
        super().__init__()
        if super().str_validate("name", name):
            if len(name) > 50:
                raise ValueError("Invalid input data")
        self.name = name
        Amenity.amenity_registry.append(self)
    
    def update(self, name):
        if super().str_validate("name", name):
            if len(name) > 50:
                raise ValueError("Invalid input data")
        self.name = name
        super().save()
        return True
    
    def delete(self, id):
        amenity_to_delete = None
        for amenity in Amenity.amenity_registry:
            if amenity.id == id:
                amenity_to_delete = amenity
                break
        if amenity_to_delete:
            Amenity.amenity_registry.remove(amenity_to_delete)
            return { 'name': amenity_to_delete.name }
        else:
            raise ValueError(f"Amenity with id {id} not found.")
    
    def to_dict(self):
        """Convert the Amenity object into a dictionary format."""
        return {
            'id': self.id,
            'name': self.name,
        }

    #Devuelve lista de usuarios
    @staticmethod
    def get_amenities():
        return [amenity.to_dict() for amenity in Amenity.amenity_registry]
    
from . import BaseModel

class Amenity(BaseModel):

    amenity_registry = []

    def __init__(self, name):
        super().__init__()
        if len(name) > 50:
            raise ValueError("Maximum length of 50 characters.")
        self.name = name
        Amenity.amenity_registry.append(self) #Agrega la nueva Amenity a la lista de Amenities
    
    def update(self, name):
        if len(name) > 50:
            raise ValueError("Maximum length of 50 characters.")
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
    
    #Devuelve una lista de todas las Amenities
    def get_amenities():
        return Amenity.amenity_registry
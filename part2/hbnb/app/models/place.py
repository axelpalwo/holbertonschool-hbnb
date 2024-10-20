from . import BaseModel

class Place(BaseModel):

    list_of_places = []

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner #Obj User
        self.reviews = [] #Lista de Reviews
        self.amenities = [] #Lista de Amenities

    def create(self, title, price, latitude, longitude, owner, amenities):
        return id
    
    def update(self, id, title, description, price, amenities):
        return True
    
    def delete(id):
        return True
    
    #Agregar Review
    def add_review(self, review):
        self.reviews.append(review)

    #Agregar Amenity
    def add_amenity(self, amenity):
        self.amenities.append(amenity)
    
    #Devuelve una lista de todos los lugares
    def get_places():
        return Place.list_of_places
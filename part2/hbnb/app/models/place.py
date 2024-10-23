from . import BaseModel

class Place(BaseModel):

    list_of_places = []

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        if super().str_validate("title", title):
            if len(title) > 100:
                raise ValueError("Maximum length of 100 characters.")
            self.title = title
        # Si existe description, se valida y guarda
        if description:
            if super().str_validate("description", description):
                self.description = description
        # Validacion de precio
        if not isinstance(price, int):
            raise TypeError("Price must be a number.")
        if price < 0:
            raise ValueError("Price must be a positive number.")
        self.price = price
        if super().lat_validate(latitude):
            self.latitude = latitude
        if super().lon_validate(longitude):
            self.longitude = longitude
        if super().validate_user(owner):
            self.owner = owner #Obj User
        self.reviews = [] #Lista de Reviews
        self.amenities = [] #Lista de Amenities
    
    def update(self, id, title, description, price, amenities):
        if super().str_validate("title", title) and \
        super().str_validate("description", description) and \
        isinstance(price, int):
            if len(title) > 100:
                raise ValueError("Maximum length of 100 characters.")
            if price < 0:
                raise ValueError("Price must be a positive number.")
            places = Place.get_places()
            for place in places:
                if place.id == id:
                    place.title = title
                    place.description = description
                    place.price = price
                    if amenities:
                        place.amenities = amenities
                        super().save()
                    return True
        return False
    
    def delete(id):
        place_to_delete = None
        for place in Place.__users__:
            if place.id == id:
                place_to_delete = place
                break
        
        if place_to_delete:
            Place.__users__.remove(place_to_delete)
            return {
                'first_name': place_to_delete.first_name,
                'last_name': place_to_delete.last_name,
                'email': place_to_delete.email
            }
        else:
            raise ValueError(f"Place with id {id} not found.")
    
    #Agregar Review
    def add_review(self, review):
        self.reviews.append(review)

    #Agregar Amenity
    def add_amenity(self, amenity):
        self.amenities.append(amenity)
    
    #Devuelve una lista de todos los lugares
    def get_places():
        return Place.list_of_places
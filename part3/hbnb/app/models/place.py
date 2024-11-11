from . import BaseModel

class Place(BaseModel):

    list_of_places = []

    def __init__(self, title, description, price, latitude, longitude, owner, amenities):
        super().__init__()
        if super().str_validate("title", title):
            if len(title) > 100:
                raise ValueError("Maximum length of 100 characters.")
            self.title = title
        # If description exists it's validated
        if description:
            if super().str_validate("description", description):
                self.description = description
        # Price validation
        if not isinstance(price, float):
            raise TypeError("Price must be a number.")
        if price < 0:
            raise ValueError("Price must be a positive number.")
        self.price = price
        if super().lat_validate(latitude):
            self.latitude = latitude
        if super().lon_validate(longitude):
            self.longitude = longitude
        self.owner = owner #User Obj
        self.reviews = [] #Reviews List
        self.amenities = amenities
        Place.list_of_places.append(self)
    
    def update(self, data):
        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        if super().str_validate("title", title) and \
        super().str_validate("description", description) and \
        isinstance(price, float):
            if len(title) > 100:
                raise ValueError("Maximum length of 100 characters.")
            if price < 0:
                raise ValueError("Price must be a positive number.")
            self.title = title
            self.description = description
            self.price = price
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
    
    # Adds a Place's Review
    def add_review(self, review):
        self.reviews.append(review)

    # Adds a Place's Amenity
    def add_amenity(self, amenity):
        self.amenities.append(amenity)
    
    def to_dict(self):
        """Convert the Place object into a dictionary format."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner,
            'amenities': self.amenities
        }

    # Returns a list from all places
    @staticmethod
    def get_places():
        return Place.list_of_places

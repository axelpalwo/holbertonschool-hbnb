import uuid
from datetime import datetime
from validate_email_address import validate_email
from user import User
from place import Place

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def str_validate(self, data_name, string):
        if not isinstance(string, str) or string == '':
            raise TypeError(f"Expected a non-empty string in {data_name}")
        return True
    
    def rating_validate(self, rating):
        if isinstance(int, rating):
            if rating < 1 or rating > 5:
                raise ValueError(f"The rating should be between 0 and 5")
            return True
        else:
            raise TypeError("Rating should be a number")
    
    def email_validate(self, email):
        if not validate_email(email):
            raise ValueError("Invalid email address")
        return True
    
    def lon_validate(self, longitude):
        if longitude < -180 or longitude > 180:
            raise ValueError("Invalid longitude")
        return True
    
    def lat_validate(self, latitude):
        if latitude < -90 or latitude > 90:
            raise ValueError("Invalid latitude")
        return True
    
    def validate_user(self, userObj):
        user_list = User.get_user_list()
        for user in user_list:
            if user.id == userObj.id:
                return True
        return False
    
    def validate_place(self, place):
        place_list = Place.get_places()
        for placelisted in place_list:
            if placelisted.id == place.id:
                return True
        return False


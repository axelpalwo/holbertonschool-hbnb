import uuid
from datetime import datetime
from validate_email_address import validate_email

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
        if not isinstance(string, str):
            raise TypeError("Invalid input data")
        elif string == '':
            raise ValueError("Invalid input data")
        return True
    
    def rating_validate(self, rating):
        if isinstance(rating, int):
            if rating < 1 or rating > 5:
                raise ValueError("Invalid input data")
            return True
        else:
            raise TypeError("Invalid input data")
    
    def email_validate(self, email):
        if not validate_email(email):
            raise ValueError("Invalid input data")
        return True
    
    def lon_validate(self, longitude):
        if longitude < -180 or longitude > 180:
            raise ValueError("Invalid input data")
        return True
    
    def lat_validate(self, latitude):
        if latitude < -90 or latitude > 90:
            raise ValueError("Invalid input data")
        return True



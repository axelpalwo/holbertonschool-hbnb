from . import BaseModel

class Review(BaseModel):

    review_list = []

    def __init__(self, text, rating, place, user):
        super().__init__()
        if super().str_validate("review text", text):
            self.text = text
        if super().rating_validate(rating):
            self.rating = rating
        self.place = place
        self.user = user
        Review.review_list.append(self) #Agrega una Review al crearse a la lista de clase

    def update(self, data):
        text = data.get('text')
        rating = data.get('rating')
        print(f"El string esta validado: {super().str_validate('text', text)}")
        print(f"El rating esta validado: {super().rating_validate(rating)}")
        if super().str_validate("text", text) and super().rating_validate(rating):
            print("Estoy modificando los datos")
            self.rating = rating
            self.text = text
            super().save()
            return True
        return False
    
    def to_dict(self):
        """Convert the Review object into a dictionary format."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user.id,
            'place_id': self.place.id
        }
    
    #Devuelve una lista de todas las Reviews
    def get_review_list():
        return Review.review_list
import unittest
from unittest.mock import patch
from app import create_app

class TestPlacesEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.review_id = None

    # GET at /reviews/ without reviews registered
    def test_get_all_reviews_with_no_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 404)

    # ================================= [POST at /reviews/] =================================
    def test_create_review(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Buuba@gmail.com"
        })
        response_owner = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Guuba@gmail.com"
        })
        if response_user.status_code == 201 and response_owner.status_code == 201:
            owner_id = response_owner.get_json().get('id')
            response_place = self.client.post('/api/v1/places/', json={
                    "title": "Cozy Apartment",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            if response_place.status_code == 201:
                place_id = response_place.get_json().get('id')
                response = self.client.post('/api/v1/reviews/', json={
                    "text": "Great place",
                    "rating": 5,
                    "user_id": response_user.get_json().get('id'),
                    "place_id": place_id
                })
            self.assertEqual(response.status_code, 201)

    # GET at /reviews/ with reviews registered
    def test_get_all_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

    def test_create_review_without_text(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Buuba2@gmail.com"
        })
        response_owner = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Guuba2@gmail.com"
        })
        if response_user.status_code == 201 and response_owner.status == 201:
            owner_id = response_owner.get_json().get('id')
            response_place = self.client.post('/api/v1/places/', json={
                    "title": "CozyT Apartment",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            if response_place.status_code == 201:
                place_id = response_place.get_json().get('id')
                response = self.client.post('/api/v1/reviews/', json={
                    "text": "",
                    "rating": 4,
                    "user_id": response_user.get_json().get('id'),
                    "place_id": place_id
                })
            self.assertEqual(response.status_code, 400)

    def test_create_review_with_wrong_user_id(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Buuba3@gmail.com"
        })
        response_owner = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Guuba3@gmail.com"
        })
        if response_user.status_code == 201 and response_owner.status == 201:
            owner_id = response_owner.get_json().get('id')
            response_place = self.client.post('/api/v1/places/', json={
                    "title": "CozyTT Apartment",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            if response_place.status_code == 201:
                place_id = response_place.get_json().get('id')
                response = self.client.post('/api/v1/reviews/', json={
                    "text": "This place is great!",
                    "rating": 4,
                    "user_id": '016a324f-0ca6-4f22-9ae1-737298445125',
                    "place_id": place_id
                })
            self.assertEqual(response.status_code, 400)

    def test_create_review_with_wrong_place_id(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Buuba4@gmail.com"
        })
        if response_user.status_code == 201:
            response = self.client.post('/api/v1/reviews/', json={
                "text": "This place is great!",
                "rating": 4,
                "user_id": response_user.get_json().get('id'),
                "place_id": '016a324f-0ca6-4f22-9ae1-737298445125'
            })
            self.assertEqual(response.status_code, 400)
    # ================================= [POST at /reviews/] =================================
    # ==================== [GET at /places/<place_id>] ====================
    def test_get_review_by_id(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Buuba9@gmail.com"
        })
        response_owner = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Guuba9@gmail.com"
        })
        if response_user.status_code == 201 and response_owner.status == 201:
            owner_id = response_owner.get_json().get('id')
            response_place = self.client.post('/api/v1/places/', json={
                    "title": "Cozy Apartment",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            if response_place.status_code == 201:
                place_id = response_place.get_json().get('id')
                response_review = self.client.post('/api/v1/reviews/', json={
                    "text": "Great place",
                    "rating": 5,
                    "user_id": response_user.get_json().get('id'),
                    "place_id": place_id
                })
            if response_review.status_code == 201:
                review_id = response_review.get_json().get('id')
                response = self.client.get(f'/api/v1/reviews/{review_id}')
                self.assertEqual(response.status_code, 200)

    def test_get_review_by_id_with_wrong_id(self):
        response = self.client.get('/api/v1/reviews/60b89e57-be39-4192-b8c8-55cb582fc468')
        self.assertEqual(response.status_code, 404)
    # ==================== [GET at /places/<place_id>] ====================
    # ==================== [PUT at /places/<place_id>] ====================
    def test_update_review_by_id(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Buuba8@gmail.com"
        })
        response_owner = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Guuba8@gmail.com"
        })
        if response_user.status_code == 201 and response_owner.status == 201:
            owner_id = response_owner.get_json().get('id')
            response_place = self.client.post('/api/v1/places/', json={
                    "title": "Cozy Apartment",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            if response_place.status_code == 201:
                place_id = response_place.get_json().get('id')
                response_review = self.client.post('/api/v1/reviews/', json={
                    "text": "Great place",
                    "rating": 5,
                    "user_id": response_user.get_json().get('id'),
                    "place_id": place_id
                })
            if response_review.status_code == 201:
                review_id = response_review.get_json().get('id')
                response = self.client.put(f'/api/v1/reviews/{review_id}', json={
                    "text": "Not so great place",
                    "rating": 2
                })
                self.assertEqual(response.status_code, 200)

    def test_update_review_by_id_empty_text(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Buuba80@gmail.com"
        })
        response_owner = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Guuba80@gmail.com"
        })
        if response_user.status_code == 201 and response_owner.status == 201:
            owner_id = response_owner.get_json().get('id')
            response_place = self.client.post('/api/v1/places/', json={
                    "title": "Cozy Apartment",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            if response_place.status_code == 201:
                place_id = response_place.get_json().get('id')
                response_review = self.client.post('/api/v1/reviews/', json={
                    "text": "Great place",
                    "rating": 5,
                    "user_id": response_user.get_json().get('id'),
                    "place_id": place_id
                })
            if response_review.status_code == 201:
                review_id = response_review.get_json().get('id')
                response = self.client.put(f'/api/v1/reviews/{review_id}', json={
                    "text": "",
                    "rating": 2
                })
                self.assertEqual(response.status_code, 400)

    def test_update_review_by_id_with_wrong_rating(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Buuba834@gmail.com"
        })
        response_owner = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Guuba834@gmail.com"
        })
        if response_user.status_code == 201 and response_owner.status == 201:
            owner_id = response_owner.get_json().get('id')
            response_place = self.client.post('/api/v1/places/', json={
                    "title": "Cozy Apartment",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            if response_place.status_code == 201:
                place_id = response_place.get_json().get('id')
                response_review = self.client.post('/api/v1/reviews/', json={
                    "text": "Great place",
                    "rating": 5,
                    "user_id": response_user.get_json().get('id'),
                    "place_id": place_id
                })
            if response_review.status_code == 201:
                review_id = response_review.get_json().get('id')
                response = self.client.put(f'/api/v1/reviews/{review_id}', json={
                    "text": "Not so great place",
                    "rating": 8
                })
                self.assertEqual(response.status_code, 400)

    def test_update_review_with_wrong_id(self):
        response = self.client.put('/api/v1/reviews/f8c76d6f-6527-42bc-aa94-9883734e02ba', json={
            "text": "Awesome place",
            "rating": 5
        })
        self.assertEqual(response.status_code, 404)

    # ==================== [PUT at /places/<place_id>] ====================
    # =================== [DELETE at /places/<place_id>] ===================
    def test_delete_review_by_id(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Buuba888@gmail.com"
        })
        response_owner = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Guuba888@gmail.com"
        })
        if response_user.status_code == 201 and response_owner.status == 201:
            owner_id = response_owner.get_json().get('id')
            response_place = self.client.post('/api/v1/places/', json={
                    "title": "Cozy Apartment",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            if response_place.status_code == 201:
                place_id = response_place.get_json().get('id')
                response_review = self.client.post('/api/v1/reviews/', json={
                    "text": "Great place",
                    "rating": 5,
                    "user_id": response_user.get_json().get('id'),
                    "place_id": place_id
                })
            if response_review.status_code == 201:
                review_id = response_review.get_json().get('id')
                response = self.client.delete(f'/api/v1/reviews/{review_id}')
                self.assertEqual(response.status_code, 200)

    def test_delete_review_by_id_with_wrong_id(self):
        response = self.client.delete('/api/v1/reviews/f8c76d6f-6527-42bc-aa94-9883734e02ba')
        self.assertEqual(response.status_code, 404)
    # =================== [DELETE at /places/<place_id>] ===================
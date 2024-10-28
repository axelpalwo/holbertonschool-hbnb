import unittest
from unittest.mock import patch
from app import create_app

class TestPlacesEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.place_id = None
        
    # GET at /places/ without places registered
    @patch('app.services.facade.HBnBFacade.get_all_places')
    def test_get_all_places_with_no_places(self, mock_get_places):
        mock_get_places.return_value = []

        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 404)

    # ================================= [POST at /places/] =================================

    def test_create_place(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "AlexTort@gmail.com"
        })
        if response_user.status_code == 201:
            owner_id = response_user.get_json().get('id')
            response = self.client.post('/api/v1/places/', json={
                    "title": "Cozy Apartment",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            self.assertEqual(response.status_code, 201)
    
    # GET at /places/ with places registered
    def test_get_all_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_create_place_empty_title(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alexander",
            "last_name": "Tort",
            "email": "AlexanderTort@gmail.com"
        })
        if response_user.status_code == 201:
            owner_id = response_user.get_json().get('id')
            response = self.client.post('/api/v1/places/', json={
                    "title": "",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            self.assertEqual(response.status_code, 400)

    def test_create_place_string_on_price(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alexander",
            "last_name": "Tort",
            "email": "Tort@gmail.com"
        })
        if response_user.status_code == 201:
            owner_id = response_user.get_json().get('id')
            response = self.client.post('/api/v1/places/', json={
                    "title": "Bantor House",
                    "description": "A nice place to stay",
                    "price": "Its cheap",
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            self.assertEqual(response.status_code, 400)

    def test_create_place_negative_price(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alexander",
            "last_name": "Tort",
            "email": "Ttaaa@gmail.com"
        })
        if response_user.status_code == 201:
            owner_id = response_user.get_json().get('id')
            response = self.client.post('/api/v1/places/', json={
                    "title": "Bantor House",
                    "description": "A nice place to stay",
                    "price": -50.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            self.assertEqual(response.status_code, 400)

    def test_create_place_wrong_longitude(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alexander",
            "last_name": "Tortass",
            "email": "Torta@gmail.com"
        })
        if response_user.status_code == 201:
            owner_id = response_user.get_json().get('id')
            response = self.client.post('/api/v1/places/', json={
                    "title": "Bantor House",
                    "description": "A nice place to stay",
                    "price": 70.0,
                    "latitude": 95.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            self.assertEqual(response.status_code, 400)
    
    def test_create_place_wrong_latitude(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alexander",
            "last_name": "Tortass",
            "email": "Tortassss@gmail.com"
        })
        if response_user.status_code == 201:
            owner_id = response_user.get_json().get('id')
            response = self.client.post('/api/v1/places/', json={
                    "title": "Bantor House",
                    "description": "A nice place to stay",
                    "price": 50.0,
                    "latitude": 37.7749,
                    "longitude": -199.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            self.assertEqual(response.status_code, 400)

    # ================================= [POST at /places/] =================================
    # =========================== [Requests at /places/<place_id>] ===========================

    # ==================== [GET at /places/<place_id>] ====================
    def test_get_place_by_id(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Roberto@gmail.com"
        })
        if response_user.status_code == 201:
            owner_id = response_user.get_json().get('id')
            response_place = self.client.post('/api/v1/places/', json={
                    "title": "RobertLand",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            if response_place.status_code == 201:
                place_id = response_place.get_json().get('id')
                response = self.client.get(f'/api/v1/places/{place_id}')
                self.assertEqual(response.status_code, 200)

    def test_get_place_by_id_with_wrong_id(self):
        response = self.client.get('/api/v1/places/016a324f-0ca6-4f22-9ae1-737298445125')
        self.assertEqual(response.status_code, 404)
    # ==================== [GET at /places/<place_id>] ====================
    # ==================== [PUT at /places/<place_id>] ====================
    def test_update_place_by_id(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Roberto222@gmail.com"
        })
        if response_user.status_code == 201:
            owner_id = response_user.get_json().get('id')
            response_place = self.client.post('/api/v1/places/', json={
                    "title": "RobertLand222",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            if response_place.status_code == 201:
                place_id = response_place.get_json().get('id')
                response = self.client.put(f'/api/v1/places/{place_id}', json={
                    "title": "Tututu",
                    "description": "Not son great place to stay",
                    "price": 90.0
                })
                self.assertEqual(response.status_code, 200)

    def test_update_place_by_id_with_empty_title(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Roberto322@gmail.com"
        })
        if response_user.status_code == 201:
            owner_id = response_user.get_json().get('id')
            response_place = self.client.post('/api/v1/places/', json={
                    "title": "RobertLand23",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            if response_place.status_code == 201:
                place_id = response_place.get_json().get('id')
                response = self.client.put(f'/api/v1/places/{place_id}', json={
                    "title": "",
                    "description": "Not so great place to stay",
                    "price": 60.0
                })
                self.assertEqual(response.status_code, 400)

    def test_update_place_by_id_with_negative_price(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Roberto362@gmail.com"
        })
        if response_user.status_code == 201:
            owner_id = response_user.get_json().get('id')
            response_place = self.client.post('/api/v1/places/', json={
                    "title": "RobertLa66nd23",
                    "description": "A nice place to stay",
                    "price": 100.0,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "owner_id": owner_id,
                    "amenities": []
            })
            if response_place.status_code == 201:
                place_id = response_place.get_json().get('id')
                response = self.client.put(f'/api/v1/places/{place_id}', json={
                    "title": "Tututrara",
                    "description": "Not so great place to stay",
                    "price": -60.0
                })
                self.assertEqual(response.status_code, 400)

    def test_update_place_wrong_id(self):
        response = self.client.put('/api/v1/places/016a324f-0ca6-4f22-9ae1-737298445125', json={
            "title": "Cobat House",
            "description": "Awesome place to spend the night",
            "price": 65.0
        })
        self.assertEqual(response.status_code, 404)
    # ==================== [PUT at /places/<place_id>] ====================
    # =========================== [Requests at /places/<place_id>] ===========================
    def test_reviews_by_place(self):
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Buu888@gmail.com"
        })
        response_owner = self.client.post('/api/v1/users/', json={
            "first_name": "Alex",
            "last_name": "Tort",
            "email": "Guu888@gmail.com"
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
                response_review_1 = self.client.post('/api/v1/reviews/', json={
                    "text": "Great place",
                    "rating": 5,
                    "user_id": response_user.get_json().get('id'),
                    "place_id": place_id
                })
                response_review_2 = self.client.post('/api/v1/reviews/', json={
                    "text": "Awesome place",
                    "rating": 5,
                    "user_id": response_user.get_json().get('id'),
                    "place_id": place_id
                })
            if response_review_1.status_code == 201 and response_review_2.status_code == 201:
                response = self.client.get(f'/api/v1/places/{place_id}/reviews')
                self.assertEqual(response.status_code, 200)

    def test_reviews_by_place_with_wrong_place_id(self):
        response = self.client.get('/api/v1/places/016a324f-0ca6-4f22-9ae1-737298445125/reviews')
        self.assertEqual(response.status_code, 404)
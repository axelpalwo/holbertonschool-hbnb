import unittest
from app import create_app

class TestAmenitiesEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.amenity_id = None
        
    # GET at /amenities/ without amenities registered
    def test_get_all_amenities_with_no_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 404)

    # ================================= [POST at /amenities/] =================================

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.amenity_id = response.get_json().get('id')
        self.assertEqual(response.status_code, 201)

    # GET at /amenities/ with amenities registered
    def test_get_all_amenities_with_no_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test_create_amenity_with_no_name(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_with_name_too_long(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WAAAAAAAAAAAAAAAATTTTTTTTTTTTTEEEEEEEEEEEERRRRRRRRRR"
        })
        self.assertEqual(response.status_code, 400)

    # ================================= [POST at /amenities/] =================================
    # ========================== [Requests at /amenities/<amenity_id>] ==========================

    # ============== [GET at /amenities/<amenity_id>] ==============

    def test_get_amenity_data(self):
        new_amenity_response = self.client.post('/api/v1/amenities/', json={
            "name": "Pool"
        })
        self.amenity_id = new_amenity_response.get_json().get('id')

        response = self.client.get(f'/api/v1/amenities/{self.amenity_id}')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity_data_when_doesnt_exist(self):
        response = self.client.get('/api/v1/amenities/016a324f-0ca6-4f22-7um3-737298445125')
        self.assertEqual(response.status_code, 404)
    
    # ============== [GET at /amenities/<amenity_id>] ==============
    # ============== [PUT at /amenities/<amenity_id>] ==============

    def test_update_amenity_data(self):
        new_amenity_response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.amenity_id = new_amenity_response.get_json().get('id')

        response = self.client.put(f'/api/v1/amenities/{self.amenity_id}', json={
            "name": "Kitchen"
        })
        self.assertEqual(response.status_code, 200)

    def test_update_amenity_data_with_wrong_id(self):
        response = self.client.put('/api/v1/amenities/016a324f-0ca6-4f22-7um3-737298445125', json={
            "name": "Tennis court"
        })
        self.assertEqual(response.status_code, 404)

    def test_update_amenity_data_empty_name(self):
        new_amenity_response = self.client.post('/api/v1/amenities/', json={
            "name": "Bowling"
        })
        self.amenity_id = new_amenity_response.get_json().get('id')

        response = self.client.put(f'/api/v1/amenities/{self.amenity_id}', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_update_amenity_data_name_too_long(self):
        new_amenity_response = self.client.post('/api/v1/amenities/', json={
            "name": "Jacuzzi"
        })
        self.amenity_id = new_amenity_response.get_json().get('id')

        response = self.client.put(f'/api/v1/amenities/{self.amenity_id}', json={
            "name": "Jaaaaaaaaaaaaaaaaaaacccccccccccccuuuuzzzzzzzzziiiiiiiiii"
        })
        self.assertEqual(response.status_code, 400)
    # ============== [PUT at /amenities/<amenity_id>] ==============
    # ============ [DELETE at /amenities/<amenity_id>] ============
    def test_delete_amenity_data(self):
        new_amenity_response = self.client.post('/api/v1/amenities/', json={
            "name": "Air Conditioner"
        })
        self.amenity_id = new_amenity_response.get_json().get('id')

        response = self.client.delete(f'/api/v1/amenities/{self.amenity_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_amenity_data_wrong_id(self):
        response = self.client.delete('/api/v1/amenities/016a324f-0ca6-4f22-7um3-737298445125')
        self.assertEqual(response.status_code, 404)
    # ============ [DELETE at /amenities/<amenity_id>] ============
    # ========================== [Requests at /amenities/<amenity_id>] ==========================
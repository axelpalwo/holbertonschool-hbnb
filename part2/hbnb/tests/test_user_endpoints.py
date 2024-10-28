import unittest
from unittest.mock import patch
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.user_id = None


    # GET /users/ with no Users
    @patch('app.services.facade.HBnBFacade.get_users_list')
    def test_get_all_users_with_no_users(self, mock_get_users):
        mock_get_users.return_value = []
        
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 404)

    # ================================= [POST at /users/] =================================
    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    # GET at /users/ with users registered
    def test_get_all_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

    def test_create_user_email_already_used(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 409)
    
    def test_create_user_invalid_firstname(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Bugarin",
            "email": "PabloBugarin@gmail.com"
        })
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_invalid_lastname(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Pablo",
            "last_name": 5,
            "email": "PabloBugarin@gmail.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Pablo",
            "last_name": "Bugarin",
            "email": "PabloBugaringmail.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": ""
        })
        self.assertEqual(response.status_code, 400)
    
    # ================================= [POST at /users/] =================================
    # ============================= [GET at /users/<user_id>] =============================

    def test_get_user_data(self):
        new_user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Ale",
            "last_name": "MontGomery",
            "email": "AleMontGomery@gmail.com"
        })
        self.user_id = new_user_response.get_json().get('id')

        response = self.client.get(f'/api/v1/users/{self.user_id}')
        self.assertEqual(response.status_code, 200)

    def test_get_user_data_not_created(self):
        response = self.client.get('/api/v1/users/016a324f-0ca6-4f22-9ae1-737298445125')
        self.assertEqual(response.status_code, 404)

    # ============================= [GET at /users/<user_id>] =============================
    # ============================= [PUT at /users/<user_id>] =============================
    def test_update_user_data(self):
        new_user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Ale",
            "last_name": "MontGomery",
            "email": "AleGomery@gmail.com"
        })
        self.user_id = new_user_response.get_json().get('id')
        response = self.client.put(f'/api/v1/users/{self.user_id}', json={
            "first_name": "Axel",
            "last_name": "Palombo",
            "email": "Axel.palombo.ap@gmail.com"
        })
        self.assertEqual(response.status_code, 200)

    def test_update_user_data_wrong_user(self):
        response = self.client.put('/api/v1/users/016a324f-0ca6-4f22-9ae1-737298445125', json={
            "first_name": "Axel",
            "last_name": "Palombo",
            "email": "Axel.palombo.ap@gmail.com"
        })
        self.assertEqual(response.status_code, 404)

    def test_update_user_data_with_bad_firstname(self):
        new_user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Ale",
            "last_name": "MontGomery",
            "email": "AleMontGoy@gmail.com"
        })
        self.user_id = new_user_response.get_json().get('id')
        response = self.client.put(f'/api/v1/users/{self.user_id}', json={
            "first_name": 5,
            "last_name": "Bugarin",
            "email": "Axel.palombo.ap@gmail.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_user_data_with_bad_lastname(self):
        new_user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Ale",
            "last_name": "MontGomery",
            "email": "MontGomery@gmail.com"
        })
        self.user_id = new_user_response.get_json().get('id')
        response = self.client.put(f'/api/v1/users/{self.user_id}', json={
            "first_name": "Pablo",
            "last_name": "",
            "email": "Axel.palombo.ap@gmail.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_user_data_with_bad_email(self):
        new_user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Ale",
            "last_name": "MontGomery",
            "email": "AleG@gmail.com"
        })
        self.user_id = new_user_response.get_json().get('id')
        response = self.client.put(f'/api/v1/users/{self.user_id}', json={
            "first_name": "Pablo",
            "last_name": "",
            "email": None
        })
        self.assertEqual(response.status_code, 400)

    # ============================= [PUT at /users/<user_id>] =============================
    # ============================ [DELETE at /users/<user_id>] ============================

    def test_delete_user_data_wrong_user(self):
        response = self.client.delete('/api/v1/users/016a324f-0ca6-4f22-9ae1-737298445125')
        self.assertEqual(response.status_code, 404)

    def test_delete_user_data(self):
        new_user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Ale",
            "last_name": "MontGomery",
            "email": "AMG@gmail.com"
        })
        self.user_id = new_user_response.get_json().get('id')
        response = self.client.delete(f'/api/v1/users/{self.user_id}')
        self.assertEqual(response.status_code, 200)

    # ============================ [DELETE at /users/<user_id>] ============================
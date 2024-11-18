from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from functools import wraps

def admin_required(func):
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return jsonify({"error": "Admin privileges required"}), 403
        return func(*args, **kwargs)
    return wrapper

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# POST Sign up -> Checks Email registration / GET all User list
@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Email already registered')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 409
        try:
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
        except TypeError as e:
            return {'error': str(e)}, 400
        except ValueError as e:
            return {'error': str(e)}, 400
        
    @api.response(200, 'Users successfully retrieved')
    @api.response(404, 'No users found')
    def get(self):
        """Get all users"""
        users_list = facade.get_users_list()
        if not users_list:
            return { 'error': 'No users found'}, 404
        return users_list, 200
        
# GET User by ID
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'You cannot modify email or password')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """Updates a User"""
        current_user = get_jwt_identity()
        user_data = api.payload

        # Verificar si el usuario existe
        existing_user = facade.get_user(user_id)
        if not existing_user:
            return {'error': 'User not found'}, 404

        # Verificar permisos para modificar datos
        is_admin = current_user.get('is_admin', False)
        if current_user['id'] != user_id and not is_admin:
            return {'error': 'Unauthorized action'}, 403

        # Validar cambios en email o contraseña (solo admin puede modificar)
        email_changed = user_data.get('email') and user_data['email'] != existing_user.email
        password_changed = user_data.get('password') and user_data['password'] != existing_user.password

        if (email_changed or password_changed) and not is_admin:
            return {'error': 'You cannot modify email or password'}, 400

        if email_changed:
            email_exist = facade.get_user_by_email(user_data['email'])
            if email_exist:
                return {'error': 'Email already registered'}, 409
        try:
            if password_changed:
                from flask_bcrypt import Bcrypt
                bcrypt = Bcrypt()
                user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')

            facade.update_user(existing_user.id, user_data)
            return {
                'message': 'User successfully updated',
            }, 200
        except (TypeError, ValueError) as e:
            return {'error': str(e)}, 400

    
    @api.response(200, 'User details deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        facade.delete_user(user_id)
        return { 'message': 'User details deleted successfully'}, 200

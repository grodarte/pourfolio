#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, session
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import User, Spirit, Cocktail

# Views go here!
class Signup(Resource):

    def post(self):
        json = request.get_json()

        if 'username' not in json or 'password' not in json:
            return {'error':'Username and password are requried.'}, 400

        try:
            user = User(
                username=json['username']
            )
            user.password_hash = json['password']
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            print(f"Session after signup: {session}")
            return user.to_dict(rules=('-password_hash',)), 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class Login(Resource):

    def post(self):
        try:
            json = request.get_json()
            if not json:
                return {'error': 'Invalid input'}, 400

            username = json.get('username')
            user = User.query.filter_by(username=username).first()
            if user and user.authenticate(json.get('password')):
                session['user_id'] = user.id
                user_dict = {
                    'id': user.id,
                    'username': user.username,
                    'spirits': [
                        {
                            'id': spirit.id,
                            'name': spirit.name,
                            'cocktails': [
                                {
                                    'id': cocktail.id,
                                    'name': cocktail.name,
                                    'ingredients': cocktail.ingredients,
                                    'instructions': cocktail.instructions
                                }
                                for cocktail in spirit.cocktails if cocktail.user_id == user.id
                            ]
                        }
                        for spirit in user.spirits
                    ]
                }
                return user_dict, 200

        
            return {'error': 'incorrect username or password'}, 401
        
        except Exception as e:
            # Log error details for debugging
            print(f"Login error: {e}")
            return {'error': 'An error occurred during login'}, 500

class CheckSession(Resource):

    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {'user': 'Not logged in'}, 401
        
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {'error': 'User not found'}, 404
        
        user_dict = {
            'id': user.id,
            'username': user.username,
            'spirits': [
                {
                    'id': spirit.id,
                    'name': spirit.name,
                    'cocktails': [
                        {
                            'id': cocktail.id,
                            'name': cocktail.name,
                            'ingredients': cocktail.ingredients,
                            'instructions': cocktail.instructions
                        }
                        for cocktail in spirit.cocktails if cocktail.user_id == user.id
                    ]
                }
                for spirit in user.spirits
            ]
        }
        return user_dict, 200

class Logout(Resource):

    def delete(self):
        if session.get('user_id'):
            try:
                session['user_id'] = None
                return {}, 204
            except Exception as e:
                return {'error': e}, 401
        else:
            return {'error': 'No user is  currently logged in'}, 400

class SpiritResource(Resource):

    def get(self):
        if session.get('user_id'):
            try:
                spirit_dicts = [{'id': spirit.id, 'name': spirit.name} for spirit in Spirit.query.all()]
                return spirit_dicts, 200
            except Exception as e:
                return {'errors': ['validation errors', str(e)]}, 400

        else:
            return {'error': 'Unauthorized to access this resource'}, 401

    def post(self):
        if session.get('user_id'):
            try:
                json = request.get_json()
                new_spirit = Spirit(name=json['name'])
                db.session.add(new_spirit)
                db.session.commit()

                return new_spirit.to_dict(), 201
            except Exception as e:
                return {'errors': ['validation errors', str(e)]}, 400
        else:
            return {'error': 'Unauthorized to access this resource'}, 401

class CocktailResource(Resource):

    def post(self):
        user_id = session.get("user_id")
        if user_id:
            try:
                json = request.get_json()
                new_cocktail = Cocktail(
                    name=json['name'],
                    ingredients=json['ingredients'],
                    instructions=json['instructions'],
                    user_id=user_id,
                    spirit_id=json['spirit_id']
                )
                db.session.add(new_cocktail)
                db.session.commit()
                return new_cocktail.to_dict(), 201
            except Exception as e:
                return {'errors':['validation errors', str(e)]}, 400
        else:
            return {'error': 'Unauthorized to access this resource'}, 401


@app.route('/')
def index():
    return '<h1>Project Server</h1>'

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(SpiritResource, '/spirits', endpoint='spirits')
api.add_resource(CocktailResource, '/cocktails', endpoint='cocktails')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
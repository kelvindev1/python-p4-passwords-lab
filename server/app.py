#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):
    def delete(self):
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204
api.add_resource(ClearSession, '/clear', endpoint='clear')



class Signup(Resource):
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201
api.add_resource(Signup, '/signup', endpoint='signup')



class CheckSession(Resource):
    def get(self):
        user = session.get("user_id")
        if not user:
            return {}, 204
        else:
            user = User.query.filter(User.id == session.get('user_id')).first()
            return user.to_dict(), 200
api.add_resource(CheckSession, '/check_session', endpoint='check_session')



class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        if not user:
            return {}, 401
        else:
            password = data.get('password')
            if user.authenticate(password):
                session['user_id'] = user.id
                return user.to_dict(), 200
api.add_resource(Login, '/login', endpoint='login')
            


class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204
api.add_resource(Logout, '/logout', endpoint='logout')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

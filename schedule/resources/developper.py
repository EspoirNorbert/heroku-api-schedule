from flask import jsonify,make_response,request
from schedule.models import *
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token


class DevelopperController():

    def register(request):
        data = request.get_json(force=True) 
        user = Developper.query.filter_by(email=data['email']).first()
        if not user:
            try:
                #hash password
                hashed_password = generate_password_hash(data['password'], method='sha256')
                developper = Developper(name=data['name'], email=data['email'], password=hashed_password)
                db.session.add(developper)
                db.session.commit()
                responseObject = {'status': 'success','message': 'Successfully registered.'} 
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                   return make_response(jsonify(message=str(e))), 500
        else:
            response = {'message': 'User already exists. Please login.'}
            return make_response(jsonify(response)), 202
    
    def login(request):
        try:
            data = request.get_json(force=True)  
            auth = Developper.query.filter_by(email=data['login']).first()     
            if auth:
                if check_password_hash(auth.password, data['password']):
                    access_token = create_access_token(identity=auth.id)
                    auth_info = {'id': auth.id, 'email': auth.email,'name':auth.name }
                    auth.api_key = access_token
                    db.session.add(auth)
                    db.session.commit()
                    return make_response(jsonify(status='Successfully',token=access_token,auth=auth_info))     
                else:
                   return make_response(jsonify(message='Invalid email or password', status='failed')), 401
            else:
                response = {'message': "user don't exist"}
                return make_response(jsonify(response)), 404
        except Exception as e:
              return make_response(jsonify(message =str(e))), 500


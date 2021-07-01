from flask import jsonify
from schedule.models import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

def authenticate(request):

    login = request['login']
    password = request['password']
    
    if not login or not password:
        {'status': 'Failed', 'message': 'login and password obligatoire'}
     
    #fin user in database
    user = User.query.filter(User.email == login).first()
    if user:
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return {'status':'Successfully', "token": access_token,"user": User.json(user)}
        else:
            return {'status': 'Failed', 'message': 'login and password incorrect'}
    else:
        return {'status': 'Failed', 'message': "user don't exist"}
        
            
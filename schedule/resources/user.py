from flask import jsonify,make_response
from schedule.models import *
from werkzeug.security import generate_password_hash , check_password_hash
from flask_jwt_extended import create_access_token

class UserController():

    def get_all_users():
        users = User.query.order_by(User.id.desc()).all()
        return make_response(jsonify(users= [UserController.json(u) for u in users],count=len(users))),200 

    def json(user):
        return {'id':user.id,'lastname':user.lastname,'firstname': user.firstname,'email': user.email,'gender':user.gender,'type':user.type,'image':UserController.generate_image(user.email)}
    
    def generate_image(email):
        return "https://i.pravatar.cc/150?u={}".format(email)

    def get_user(user_id):
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                return make_response(jsonify(user= UserController.json(user))),200 
            else:
                return make_response(jsonify(message="user dont exists", status="failed")),401
        except Exception as e:
            return make_response(jsonify(message= str(e))),500
 
    def get_total_user():
        total = User.query.count()
        return make_response(jsonify(total_user=total)),200
    
    def add_admin(request):
        data = request.get_json(force=True)
        #get data from api
        firstname = data['firstname'] #firstname
        lastname = data['lastname'] #lastname
        email = data['email'] #email
        gender = data['gender'] #gender
        password = data['password'] #password
        try:
            admin = UserController.add_user(firstname,lastname,email,gender,password,"admin")
            if admin != 0:
                return make_response(jsonify(message='admin create successfully', status='success' )),200
            else:
                return make_response(jsonify(message='admin already exist', status='failed' )),202
        except Exception as e:
                return make_response(jsonify(str(e))),500

    def add_user(firstname,lastname,email,gender,password,type):
        try:
            #get exiting user
            user = User.query.filter_by(email=email).first()
            #dont find user 
            if user is None:
                new_user = User(lastname=lastname,firstname=firstname,email=email,gender=gender,password=generate_password_hash(password),type=type)
                db.session.add(new_user)
                db.session.commit()
                return new_user.id
            elif user.email == email:
                return 0
        except Exception as e:
               return print(e)

    def update_user(firstname,lastname,email,gender,password,type):
        pass

    def authenticate(request):
        try:
            data = request.get_json(force=True) 
            auth = User.query.filter_by(email=data['login']).first()
                   
            if auth:
                if check_password_hash(auth.password, data['password']):
                    access_token = create_access_token(identity=auth.id)
                    return make_response(jsonify(status='Successfully',token=access_token,auth=UserController.json(auth)))     
                else:
                   return make_response(jsonify(message='Invalid email or password', status='failed')), 401
            else:
                return make_response(jsonify(message= "user don't exist")), 404
        except Exception as e:
              return make_response(jsonify(message = 'xx' + str(e))), 500


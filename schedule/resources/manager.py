from flask import jsonify,make_response
from sqlalchemy.exc import SQLAlchemyError
from schedule.models import *
from schedule.resources.user import UserController

class ManagerController():

    def get_all_manager():
        managers = db.session.query(Manager,User).select_from(Manager).join(User).order_by(Manager.id.desc()).all()
        return make_response(jsonify(managers= [ManagerController.json(manager,user) for manager,user in managers] ,count=len(managers))),200 

    def get_manager_classroom(manager_id):
        try:
            existing_manager = Manager.query.filter_by(id=manager_id).first()
            if existing_manager:
                classrooms =ManagerController.get_classroom(manager_id)
                return make_response(jsonify(classrooms= classrooms ,total_classroom=len(classrooms))),200 
            else:
                return make_response(jsonify(status='failed', message="Manager doen't exist")),401 
        except SQLAlchemyError as e: 
               return make_response(jsonify(message= str(e))),500

    def get_total_manager():
        total = Manager.query.count()
        return make_response(jsonify(total_manager=total)),200
    
    def get_classroom(manager_id):
        return [classroom.name for classroom in Classroom.query.join(Manager).filter(Manager.id==manager_id).all()]

    def json(manager,user):
        return {'id':manager.id,'title': manager.title,'lastname':user.lastname,'firstname':user.firstname,'email': user.email,'gender':user.gender,'image':'https://i.pravatar.cc/150?u={}'.format(user.email),'classrooms':ManagerController.get_classroom(manager.id)}
    
    def add_manager(request):
        try:
            data = request.get_json(force=True)
            #get data from api
            firstname = data['firstname'] #firstname
            lastname = data['lastname'] #lastname
            email = data['email'] #email
            gender = data['gender'] #gender
            title = data['title'] #title
            password = data['password'] #password
            #add user
            user_id = UserController.add_user(firstname,lastname,email,gender,password,"manager")
            #dont find user 
            if user_id != 0:
                try:
                    new_manager = Manager(title=title,user_id=user_id)
                    db.session.add(new_manager)
                    db.session.commit()
                    return make_response(jsonify(status='success', message='manager created successfully' )),401 
                except Exception as e:
                    db.session.rollback()
                    return make_response(jsonify(status='failed', message=str(e))),401           
            else:
               return make_response(jsonify(message='user already exist', status='failed')),202
        except SQLAlchemyError as e:
               return make_response(jsonify(message= str(e))),500
            
    def get_manager(manager_id):
        try:
            manager = db.session.query(User,Manager,Classroom).select_from(User).join(Manager).join(Classroom).filter(Manager.id ==manager_id).first()
            if manager:
                return make_response(jsonify(manager= ManagerController.json(manager.Manager,manager.User))),200 
            else:
                return make_response(jsonify(message="manager dont exists", status="failed")),401
        except SQLAlchemyError as e:
            return make_response(jsonify(message= str(e))),500
    
    def update_manager(request):
        return make_response(jsonify(message= 'manager updated successfully',status='success')),200
        
    def delete_manager(_id):
        return make_response(jsonify(message= 'manager deleted successfully' , status='success')),200
        

from flask import jsonify,make_response
from sqlalchemy.exc import SQLAlchemyError
from schedule.models import *

class ClassroomController():

    def get_all_classroom():
        classrooms = db.session.query(Classroom,Manager,User).select_from(Classroom).join(Manager).join(User).order_by(Classroom.id.desc()).all()
        return make_response(jsonify(classrooms= [ClassroomController.json(classroom,manager,user) for classroom,manager,user in classrooms] ,count=len(classrooms))),200 

    def get_total_classroom():
        total = Classroom.query.count()
        return make_response(jsonify(total_classroom=total)),200

    def json(classroom,manager,user):
        return {'id':classroom.id,'name':classroom.name,'lastname':user.lastname,'manager':{'lastname':user.lastname,'firstname':user.firstname,'title':manager.title}}
 
    def add_classroom(request):
        try:
            data = request.get_json(force=True)
            #get data from api
            name = data['name']
            manager = data['manager']
            print(name)
            #check if classroom exist
            existing_manager = Manager.query.join(User).filter(User.firstname.__eq__(manager)).first()
            if existing_manager:
                #check if classroom existing
                existing_classroom = Classroom.query.filter(Classroom.name.__eq__(name)).first()
                print(existing_classroom)
                if existing_classroom is None:
                    try:
                        new_classroom = Classroom(name=name, manager_id=existing_manager.id)
                        db.session.add(new_classroom) 
                        db.session.commit()
                        return make_response(jsonify(status='success', message='classroom created successfully' )),201 
                    except Exception as e:
                        db.session.rollback()
                        return make_response(jsonify(status='failed', message=str(e))),401 
                else:
                    return make_response(jsonify(status='failed', message="classroom already exist")),202      
            else:
               return make_response(jsonify(message='manager doesn\'t exist', status='failed')),401
        except SQLAlchemyError as e:
               return make_response(jsonify(message= str(e))),500
            
    def get_classroom(classroom_id):
        try:
            classroom = db.session.query(Classroom,Manager,User).select_from(Classroom).join(Manager).join(User).filter(Classroom.id ==classroom_id).first()
            if classroom:
                return make_response(jsonify(classroom=ClassroomController.json(classroom.Classroom,classroom.Manager,classroom.User))),200 
            else:
                return make_response(jsonify(message="classroom dont exists", status="failed")),404
        except SQLAlchemyError as e:
            return make_response(jsonify(message= str(e))),500
    
    def update_classroom(request):
        return make_response(jsonify(message= 'classroom updated successfully',status='success')),200

    def delete_classroom(request):
        return make_response(jsonify(message= 'classroom deleted successfully' , status='success')),200
        





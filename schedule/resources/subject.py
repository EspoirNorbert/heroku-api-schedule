from flask import jsonify,make_response
from sqlalchemy.exc import SQLAlchemyError
from schedule.models import *

class SubjectController():

    def get_all_subject():
        subjects = db.session.query(Subject,Teacher,User).select_from(Subject).join(Teacher).join(User).order_by(Subject.id.desc()).all()
        return make_response(jsonify(subjects=[SubjectController.json(subject,teacher,user) for subject,teacher,user in subjects] ,count=len(subjects))),200 

    def get_total_subject():
        total = Subject.query.count()
        return make_response(jsonify(total_subject=total)),200

    def json(subject,teacher,user):
        return {'id':subject.id,'name':subject.name,'lastname':user.lastname,'teacher':{'lastname':user.lastname,'firstname':user.firstname,'grade':teacher.grade}}
 
    def add_subject(request):
        try:
            data = request.get_json(force=True)
            #get data from api
            name = data['name']
            teacher = data['teacher']
            coefficient = data['coefficient']
            #check if subject exist
            existing_teacher = Teacher.query.join(User).filter(User.firstname.__eq__(teacher)).first()
            if existing_teacher:
                #check if subject existing
                existing_subject = Subject.query.filter(Subject.name.__eq__(name)).first()
                if existing_subject is None:
                    try:
                        new_subject = Subject(name=name,coefficient=coefficient,teacher_id=existing_teacher.id)
                        db.session.add(new_subject) 
                        db.session.commit()
                        return make_response(jsonify(status='success', message='subject created successfully' )),401 
                    except Exception as e:
                        db.session.rollback()
                        return make_response(jsonify(status='failed', message=str(e))),401 
                else:
                    return make_response(jsonify(status='failed', message="subject already exist")),202      
            else:
               return make_response(jsonify(message='teacher dont exist', status='failed')),202
        except SQLAlchemyError as e:
               return make_response(jsonify(message= str(e))),500
            
    def get_subject(subject_id):
        try:
            subject = db.session.query(Subject,Teacher,User).select_from(Subject).join(Teacher).join(User).filter(Subject.id ==subject_id).first()
            if subject:
                return make_response(jsonify(subject= SubjectController.json(subject.Subject,subject.Teacher,subject.User))),200 
            else:
                return make_response(jsonify(message="subject dont exists", status="failed")),401
        except SQLAlchemyError as e:
            return make_response(jsonify(message= str(e))),500
    
    def update_subject(request):
        return make_response(jsonify(message= 'subject updated successfully',status='success')),200

    def delete_subject(request):
        return make_response(jsonify(message= 'subject deleted successfully' , status='success')),200
        

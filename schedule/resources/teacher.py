from flask import jsonify,make_response
from sqlalchemy.exc import SQLAlchemyError
from schedule.models import *
from schedule.resources.user import UserController

class TeacherController():

    def get_all_teacher():
        teachers = db.session.query(User,Teacher).select_from(User).join(Teacher).order_by(Teacher.id.desc()).all()
        return make_response(jsonify(teachers =[TeacherController.json(teacher,user) for user,teacher in teachers],count=len(teachers) )) 

    def get_teacher_subject(teacher_id):
        try:
            existing_teacher = Teacher.query.filter_by(id=teacher_id).first()
            if existing_teacher:
                subjects =TeacherController.get_subject(teacher_id)
                return make_response(jsonify(subjects= subjects ,total_subjects=len(subjects))),200
            else:
                return make_response(jsonify(status='failed', message="teacher doen't exist")),401 
        except SQLAlchemyError as e: 
               return make_response(jsonify(message= str(e))),500

    def get_total_teacher():
        total = Teacher.query.count()
        return make_response(jsonify(total_teacher=total)),200
    
    def get_subject(teacher_id):
        return [subject.name for subject in Subject.query.join(Teacher).filter(Teacher.id==teacher_id).all()]

    def json(teacher,user):
        return {'id':teacher.id,'grade': teacher.grade,'lastname':user.lastname,'firstname':user.firstname,'email': user.email,'gender':user.gender,'image':'https://i.pravatar.cc/150?u={}'.format(user.email),'subjects':TeacherController.get_subject(teacher.id)}
    
    def add_teacher(request):
        try:
            data = request.get_json(force=True)
            #get data from api
            firstname = data['firstname'] #firstname
            lastname = data['lastname'] #lastname
            email = data['email'] #email
            gender = data['gender'] #gender
            grade = data['grade'] #grade
            password = data['password'] #password
            #add user
            user_id = UserController.add_user(firstname,lastname,email,gender,password,"teacher")
            print(user_id)
            #dont find user 
            if user_id != 0:
                try:
                    new_teacher = Teacher(grade=grade,user_id=user_id)
                    db.session.add(new_teacher)
                    db.session.commit()
                    return make_response(jsonify(status='success', message='teacher created successfully' )),401 
                except Exception as e:
                    db.session.rollback()
                    return make_response(jsonify(status='failed', message=str(e))),401           
            else:
               return make_response(jsonify(message='user already exist', status='failed')),202
        except SQLAlchemyError as e:
               return make_response(jsonify(message= str(e))),500
            
    def get_teacher(teacher_id):
        try:
            teacher =db.session.query(User,Teacher).select_from(User).join(Teacher).filter(Teacher.id ==teacher_id).first()
            if teacher:
                return make_response(jsonify(teacher= TeacherController.json(teacher.Teacher,teacher.User))),200 
            else:
                return make_response(jsonify(message="teacher dont exists", status="failed")),401
        except SQLAlchemyError as e:
            return make_response(jsonify(message= str(e))),500
    
    def update_teacher(request):
        return make_response(jsonify(message= 'teacher updated successfully',status='success')),200
        
    def delete_teacher(_id):
        return make_response(jsonify(message= 'teacher deleted successfully' , status='success')),200
        



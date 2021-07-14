from flask import jsonify,make_response
from sqlalchemy.exc import SQLAlchemyError
from schedule.models import *
from schedule.resources.user import *
from werkzeug.security import generate_password_hash
from random import randint

class StudentController():

    def get_all_student():
        students = db.session.query(User,Student,Classroom).select_from(User).join(Student).join(Classroom).order_by(Student.id.desc()).all()
        return make_response(jsonify(students= [StudentController.json(student,user,classroom) for user,student,classroom in students] ,count=len(students))),200 

    def get_all_student_by_classroom(name):
        try:
            existing_classroom = Classroom.query.filter_by(name=name).first()
            if existing_classroom:
                students = db.session.query(User,Student,Classroom).select_from(User).join(Student).join(Classroom).filter(Classroom.name==name).order_by(Student.id.desc()).all()
                return make_response(jsonify(students= [StudentController.json(student,user,classroom) for user,student,classroom in students] ,count=len(students))),200 
            else:
                return make_response(jsonify(status='failed', message="classroom doen't exist")),401 
        except SQLAlchemyError as e: 
               return make_response(jsonify(message= str(e))),500

    def get_total_student():
        total = Student.query.count()
        return make_response(jsonify(total_student=total)),200

    def json(student,user,classroom):
        return {'id':student.id, 'number_id': student.id_number,'lastname':user.lastname,'firstname':user.firstname,'email': user.email,'gender':user.gender,'classroom': classroom.name,'image':'https://i.pravatar.cc/150?u={}'.format(user.email) }
    
    def add_student(request):
        try:
            data = request.get_json(force=True)
            #get data from api
            firstname = data['firstname'] #firstname
            lastname = data['lastname'] #lastname
            email = data['email'] #email
            gender = data['gender'] #gender
            classroom = data['classroom'] #gender
            password = data['password'] #password
            #add user
            user_id = UserController.add_user(firstname,lastname,email,gender,password,"student")
            #dont find user 
            if user_id != 0:
                #check if classroom exist
                existing_classroom = Classroom.query.filter_by(name=classroom).first()
                if existing_classroom:
                    try:
                        new_student = Student(id_number=randint(1,10000000000),classroom_id=existing_classroom.id,user_id=user_id)
                        db.session.add(new_student)
                        db.session.commit()
                        return make_response(jsonify(status='success', message='Student created successfully' )),401 
                    except Exception as e:
                        db.session.rollback()
                        return make_response(jsonify(status='failed', message=str(e))),401      
                else:
                    return make_response(jsonify(status='failed', message="classroom doen't exist")),401      
            else:
               return make_response(jsonify(message='user already exist', status='failed')),202
        except SQLAlchemyError as e:
               return make_response(jsonify(message= str(e))),500
            
    def get_student(student_id):
        try:
            student = db.session.query(User,Student,Classroom).select_from(User).join(Student).join(Classroom).filter(Student.id ==student_id).first()
            if student:
                return make_response(jsonify(student= StudentController.json(student.Student,student.User,student.Classroom))),200 
            else:
                return make_response(jsonify(message="student dont exists", status="failed")),401
        except SQLAlchemyError as e:
            return make_response(jsonify(message= str(e))),500
    
    def update_student(_id,firstname,lastname,email,gender,password,type,classroom):
        pass
    
    def delete_student(_id):
        pass
        




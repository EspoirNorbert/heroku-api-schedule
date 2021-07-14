from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import cross_origin
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required


app = Flask(__name__) #app
jwt = JWTManager(app)
app.config.from_object('config')
app.config["JWT_SECRET_KEY"] = "schedule-flask-api" 
db = SQLAlchemy(app)

from schedule.resources.user import UserController
from schedule.resources.student import StudentController
from schedule.resources.manager import ManagerController
from schedule.resources.classroom import ClassroomController
from schedule.resources.developper import DevelopperController
from schedule.resources.teacher import TeacherController
from schedule.resources.room import RoomController
from schedule.resources.course import CourseController
from schedule.resources.subject import SubjectController

@app.route('/')
@cross_origin()
def index():
    return jsonify({"message": "Welcome to truggle api school"})

@app.route('/schedule/v1/developper/signup', methods=['POST'])
@cross_origin()
def register_developper():
    return DevelopperController.register(request)

@app.route('/schedule/v1/developper/login', methods=['POST'])
@cross_origin()
def login_developper():
    return DevelopperController.login(request)

@app.route('/schedule/v1/users/auth', methods=['POST'])
@cross_origin()
@jwt_required()
def get_auth():
    return UserController.authenticate(request)

@app.route('/schedule/v1/users', methods=['GET'])
@cross_origin()
@jwt_required()
def get_users():
    return UserController.get_all_users()

@app.route('/schedule/v1/users/create', methods=['POST'])
@cross_origin()
@jwt_required()
def create_user():
    return UserController.add_admin(request)

@app.route('/schedule/v1/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@jwt_required()
def handle_user(id):
    
    if request.method == 'GET':
      return UserController.get_user(id)

    elif request.method == 'PUT':
        return UserController.update_user(request)

    elif request.method == 'DELETE':
        return UserController.delete_user(request)

@app.route('/schedule/v1/users/total', methods=['GET'])
@cross_origin()
@jwt_required()
def get_total_user():
    return UserController.get_total_user()

@app.route('/schedule/v1/students', methods=['GET'])
@cross_origin()
@jwt_required()
def get_students():
    return StudentController.get_all_student()

@app.route('/schedule/v1/students/classroom/<string:name>', methods=['GET'])
@cross_origin()
@jwt_required()
def get_student_by_classroom(name):
    return StudentController.get_all_student_by_classroom(name)

@app.route('/schedule/v1/students/create', methods=['POST'])
@cross_origin()
@jwt_required()
def create_student():
    return StudentController.add_student(request)
    
@app.route('/schedule/v1/students/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@jwt_required()
def handle_student(id):
    
    if request.method == 'GET':
      return StudentController.get_student(id)

    elif request.method == 'PUT':
        return StudentController.update_student(request)

    elif request.method == 'DELETE':
        return StudentController.delete_student(request)

@app.route('/schedule/v1/students/total', methods=['GET'])
@cross_origin()
@jwt_required()
def get_total_student():
    return StudentController.get_total_student()

@app.route('/schedule/v1/classrooms', methods=['GET'])
@cross_origin()
@jwt_required()
def get_classrooms():
    return ClassroomController.get_all_classroom()

@app.route('/schedule/v1/classrooms/create', methods=['POST'])
@cross_origin()
@jwt_required()
def create_classroom():
    return ClassroomController.add_classroom(request)

@app.route('/schedule/v1/classrooms/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@jwt_required()
def handle_classroom(id):
    
    if request.method == 'GET':
      return ClassroomController.get_classroom(id)

    elif request.method == 'PUT':
        return ClassroomController.update_classroom(request)

    elif request.method == 'DELETE':
        return ClassroomController.delete_classroom(request)

@app.route('/schedule/v1/classrooms/total', methods=['GET'])
@cross_origin()
@jwt_required()
def get_total_classroom():
    return ClassroomController.get_total_classroom()

@app.route('/schedule/v1/managers', methods=['GET'])
@cross_origin()
@jwt_required()
def get_managers():
    return ManagerController.get_all_manager()

@app.route('/schedule/v1/managers/create', methods=['POST'])
@cross_origin()
@jwt_required()
def create_manager():
    return ManagerController.add_manager(request)

@app.route('/schedule/v1/managers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@jwt_required()
def handle_manager(id):
    
    if request.method == 'GET':
      return ManagerController.get_manager(id)

    elif request.method == 'PUT':
        return ManagerController.update_manager(request)

    elif request.method == 'DELETE':
        return ManagerController.delete_manager(request)

@app.route('/schedule/v1/managers/<int:id>/classrooms', methods=['GET'])
@cross_origin()
@jwt_required()
def get_manager_classroom(id):
    return ManagerController.get_manager_classroom(id)

@app.route('/schedule/v1/managers/total', methods=['GET'])
@cross_origin()
@jwt_required()
def get_total_manager():
    return ManagerController.get_total_manager()


@app.route('/schedule/v1/teachers', methods=['GET'])
@cross_origin()
@jwt_required()
def get_teachers():
    return TeacherController.get_all_teacher()

@app.route('/schedule/v1/teachers/create', methods=['POST'])
@cross_origin()
@jwt_required()
def create_teacher():
    return TeacherController.add_teacher(request)
    
@app.route('/schedule/v1/teachers/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@jwt_required()
def handle_teacher(id):
    
    if request.method == 'GET':
      return TeacherController.get_teacher(id)

    elif request.method == 'PUT':
        return TeacherController.update_teacher(request)

    elif request.method == 'DELETE':
        return TeacherController.delete_teacher(request)

@app.route('/schedule/v1/teachers/<int:id>/subjects', methods=['GET'])
@cross_origin()
@jwt_required()
def get_teacher_subject(id):
    return TeacherController.get_teacher_subject(id)

@app.route('/schedule/v1/teachers/total', methods=['GET'])
@cross_origin()
@jwt_required()
def get_total_teacher():
    return TeacherController.get_total_teacher()

@app.route('/schedule/v1/rooms', methods=['GET'])
@cross_origin()
@jwt_required()
def get_rooms():
    return RoomController.get_all_room()

@app.route('/schedule/v1/rooms/create', methods=['POST'])
@cross_origin()
@jwt_required()
def create_room():
    return RoomController.add_room(request)
    
@app.route('/schedule/v1/rooms/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@jwt_required()
def handle_room(id):
    
    if request.method == 'GET':
      return RoomController.get_room(id)

    elif request.method == 'PUT':
        return RoomController.update_room(request)

    elif request.method == 'DELETE':
        return RoomController.delete_room(request)


@app.route('/schedule/v1/courses', methods=['GET'])
@cross_origin()
@jwt_required()
def get_courses():
    return CourseController.get_all_courses()

@app.route('/schedule/v1/courses/classroom/<string:name>', methods=['GET'])
@cross_origin()
@jwt_required()
def get_course_by_classroom(name):
    return CourseController.get_course_by_classroom(name)

@app.route('/schedule/v1/courses/create', methods=['POST'])
@cross_origin()
@jwt_required()
def create_course():
    return CourseController.add_course(request)
    
@app.route('/schedule/v1/courses/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@jwt_required()
def handle_course(id):
    
    if request.method == 'GET':
      return CourseController.get_course(id)

    elif request.method == 'PUT':
        return CourseController.update_course(request)

    elif request.method == 'DELETE':
        return CourseController.delete_course(request)

@app.route('/schedule/v1/courses/total', methods=['GET'])
@cross_origin()
@jwt_required()
def get_total_course():
    return CourseController.get_total_course()

@app.route('/schedule/v1/courses/<string:classroom>/<string:start>/<string:end>', methods=['GET'])
@cross_origin()
@jwt_required()
def get_course_classroom_by_week(classroom,start,end):
      return CourseController.get_course_by_week(classroom,start,end)



@app.route('/schedule/v1/subjects', methods=['GET'])
@cross_origin()
@jwt_required()
def get_subjects():
    return SubjectController.get_all_subject()

@app.route('/schedule/v1/subjects/create', methods=['POST'])
@cross_origin()
@jwt_required()
def create_subject():
    return SubjectController.add_subject(request)
    
@app.route('/schedule/v1/subjects/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@jwt_required()
def handle_subject(id):
    
    if request.method == 'GET':
      return SubjectController.get_subject(id)

    elif request.method == 'PUT':
        return SubjectController.update_subject(request)

    elif request.method == 'DELETE':
        return SubjectController.delete_subject(request)

@app.route('/schedule/v1/subjects/total', methods=['GET'])
@cross_origin()
@jwt_required()
def get_total_subject():
    return SubjectController.get_total_subject()

@app.route('/schedule/v1/rooms/total', methods=['GET'])
@cross_origin()
@jwt_required()
def get_total_room():
    return RoomController.get_total_room()

@app.errorhandler(404)
def route_not_found(e):
    return make_response(jsonify(message=str(e))),404

@app.errorhandler(400)
def route_not_found(e):
    return make_response(jsonify(message=str(e))),400

@app.errorhandler(405)
def route_not_found(e):
    return make_response(jsonify(message=str(e))),405

@app.errorhandler(500)
def internal_error(e):
    return make_response(jsonify(message=str(e))),500
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import JWTManager

#from resources.user import  UserController
from schedule.error import *
from schedule.auth import *

from schedule.resources.user import UserController
from schedule.resources.student import StudentController
from schedule.resources.manager import ManagerController
from schedule.resources.teacher import TeacherController
from schedule.resources.classroom import ClassroomController
from schedule.resources.room import RoomController
from schedule.resources.subject import SubjectController
from schedule.resources.course import CourseController

# Initialize Flask app with SQLAlchemy
app = Flask(__name__)
#create by
bcrypt = Bcrypt(app)
#create du jwt 
jwt = JWTManager(app)
#configuration de la base de donnee
app.config.from_object('config')
app.config["JWT_SECRET_KEY"] = "schedule-flask-api" 
#creation de la base
db = SQLAlchemy(app)

@app.route('/')
@cross_origin() # allow all origins all methods.
def index():
    return jsonify({"message": "Welcome to truggle api school"})

@app.route('/schedule/v1/login', methods=['POST'])
@cross_origin() # allow all origins all methods.
def get_auth():
    data = request.get_json(force=True)
    response = authenticate(data)
    return jsonify({"message" : response}), 200
    
#utilisateurs route api
@app.route('/schedule/v1/users', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_users():
    return jsonify({
        'Users': UserController.get_all_users() ,
        "total_users": UserController.get_total_user(),
        "success": "ok",
        })

@app.route('/schedule/v1/users/<int:id>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_user_one(id):
    return jsonify({"user": UserController.get_user(id)})

############################# Students Route  #######################################
@app.route('/schedule/v1/students', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_students():
    return jsonify({"students": StudentController.get_all_student(),"success": "ok","total_student": StudentController.get_total_student()})

@app.route('/schedule/v1/students', methods=['POST'])
@cross_origin() # allow all origins all methods.
def create_student():
    data = request.get_json(force=True)
    response = StudentController.add_student(data)
    return jsonify({"message" : response}), 201

@app.route('/schedule/v1/students/<int:id>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_student_one(id):
    return jsonify(StudentController.get_student(id))

@app.route('/schedule/v1/students/<int:id>', methods=['PUT'])
@cross_origin() # allow all origins all methods.
def update_student():
    data = request.get_json(force=True)
    response = StudentController.update_student(data)
    return jsonify({"message" : response})

@app.route('/schedule/v1/students/<int:id>', methods=['DELETE'])
@cross_origin() # allow all origins all methods.
def remove_student():
    response = StudentController.delete_student(id)
    return jsonify({"message" : response})

############################# Manager Route  #######################################
@app.route('/schedule/v1/managers', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_managers():
    return jsonify({"managers": ManagerController.get_all_manager(),"success": "ok","total_manager": ManagerController.get_total_manager()})

@app.route('/schedule/v1/managers', methods=['POST'])
@cross_origin() # allow all origins all methods.
def create_manager():
    data = request.get_json(force=True)
    response = ManagerController.add_manager(data)
    return jsonify({"message" : response})

@app.route('/schedule/v1/managers/<int:id>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_manager_one(id):
    return jsonify(ManagerController.get_manager(id))

@app.route('/schedule/v1/managers/<int:id>', methods=['PUT'])
@cross_origin() # allow all origins all methods.
def update_manager():
    data = request.get_json(force=True)
    response = StudentController.update_student(data)
    return jsonify({"message" : response})

@app.route('/schedule/v1/managers/<int:id>', methods=['DELETE'])
@cross_origin() # allow all origins all methods.
def remove_manager():
    response = ManagerController.delete_manager(id)
    return jsonify({"message" : response})

############################# Teacher Route  #######################################
@app.route('/schedule/v1/teachers', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_teachers():
    return jsonify({"teachers": TeacherController.get_all_teacher(),"success": "ok","total_teachers": TeacherController.get_total_teacher()})

@app.route('/schedule/v1/teachers', methods=['POST'])
@cross_origin() # allow all origins all methods.
def create_teacher():
    data = request.get_json(force=True)
    response = TeacherController.add_teacher(data)
    return jsonify({"message" : response})
    
@app.route('/schedule/v1/teachers/<int:id>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_teacher_one(id):
    return jsonify({"teacher": TeacherController.get_teacher(id)})

@app.route('/schedule/v1/teachers/<int:id>', methods=['PUT'])
@cross_origin() # allow all origins all methods.
def update_teacher():
    data = request.get_json(force=True)
    response = StudentController.update_student(data)
    return jsonify({"message" : response})

@app.route('/schedule/v1/teachers/<int:id>', methods=['DELETE'])
@cross_origin() # allow all origins all methods.
def remove_teacher():
    response = ManagerController.delete_manager(id)
    return jsonify({"message" : response})

############################# Classroom Route  #######################################
@app.route('/schedule/v1/classrooms', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_classrooms():
    return jsonify({"classrooms": ClassroomController.get_all_classroom(),"success": "ok","total_manager": ClassroomController.get_total_classroom()})

@app.route('/schedule/v1/classrooms', methods=['POST'])
@cross_origin() # allow all origins all methods.
def create_classroom():
    data = request.get_json(force=True)
    response = ClassroomController.add_classroom(data)
    return jsonify({"message" : response})

@app.route('/schedule/v1/classrooms/<int:id>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_classroom_one(id):
    return jsonify({"classroom": ClassroomController.get_classroom(id)})

@app.route('/schedule/v1/classrooms/<int:id>', methods=['PUT'])
@cross_origin() # allow all origins all methods.
def update_classroom():
    data = request.get_json(force=True)
    response = StudentController.update_student(data)
    return jsonify({"message" : response})

@app.route('/schedule/v1/classrooms/<int:id>', methods=['DELETE'])
@cross_origin() # allow all origins all methods.
def remove_classroom():
    response = ManagerController.delete_manager(id)
    return jsonify({"message" : response})

############################# Subject Route  #######################################
@app.route('/schedule/v1/subjects', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_subjects():
    return jsonify({"subjects": SubjectController.get_all_subject(),"success": "ok","total_subject": SubjectController.get_total_subject()})
    
@app.route('/schedule/v1/subjects', methods=['POST'])
@cross_origin() # allow all origins all methods.
def create_subject():
    data = request.get_json(force=True)
    response = SubjectController.add_subject(data)
    return jsonify({"message" : response})

@app.route('/schedule/v1/subjects/<int:id>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_subject_one(id):
    return jsonify({"subject": SubjectController.get_subject(id)})

@app.route('/schedule/v1/subjects/<int:id>', methods=['PUT'])
@cross_origin() # allow all origins all methods.
def update_subject():
    data = request.get_json(force=True)
    response = StudentController.update_student(data)
    return jsonify({"message" : response})

@app.route('/schedule/v1/subjects/<int:id>', methods=['DELETE'])
@cross_origin() # allow all origins all methods.
def remove_subject():
    response = ManagerController.delete_manager(id)
    return jsonify({"message" : response})

############################# Room Route  #######################################
@app.route('/schedule/v1/rooms', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_rooms():
    return jsonify({"rooms": RoomController.get_all_rooms(),"success": "ok","total_rooms": RoomController.get_total_room()})
    
@app.route('/schedule/v1/rooms', methods=['POST'])
@cross_origin() # allow all origins all methods.
def create_room():
    data = request.get_json(force=True)
    response = RoomController.add_room(data)
    return jsonify({"message" : response})

@app.route('/schedule/v1/rooms/<int:id>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_room_one(id):
    return jsonify({"room": RoomController.get_room(id)})

@app.route('/schedule/v1/rooms/<int:id>', methods=['PUT'])
@cross_origin() # allow all origins all methods.
def update_room():
    data = request.get_json(force=True)
    response = StudentController.update_student(data)
    return jsonify({"message" : response})

@app.route('/schedule/v1/rooms/<int:id>', methods=['DELETE'])
@cross_origin() # allow all origins all methods.
def remove_room():
    response = ManagerController.delete_manager(id)
    return jsonify({"message" : response})

############################# Courses Route  #######################################
@app.route('/schedule/v1/courses', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_courses():
    return jsonify({
        "courses": CourseController.get_all_course(),
        "success": "ok",
        "total_rooms": CourseController.get_total_course()
        })
    
@app.route('/schedule/v1/courses', methods=['POST'])
@cross_origin() # allow all origins all methods.
def create_course():
    data = request.get_json(force=True)
    response = CourseController.add_course(data)
    return jsonify({"message" : response})

@app.route('/schedule/v1/courses/<int:id>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_course_one(id):
    return jsonify({"course": CourseController.get_course(id)})

@app.route('/schedule/v1/courses/<string:name>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_course_classroom(name):
      return jsonify({"course": CourseController.get_course_by_class(name)})

@app.route('/schedule/v1/courses/<string:classroom>/<string:start>/<string:end>', methods=['GET'])
@cross_origin() # allow all origins all methods.
def get_course_classroom_by_week(classroom,start,end):
      return jsonify(
          {
              "course": CourseController.get_course_by_week(classroom,start,end), 
              "periode" : {
                "start" : start, 
                "end" : end
              }
              }
        )

@app.route('/schedule/v1/courses/<int:id>', methods=['PUT'])
@cross_origin() # allow all origins all methods.
def update_course():
    data = request.get_json(force=True)
    response = StudentController.update_student(data)
    return jsonify({"message" : response})

@app.route('/schedule/v1/courses/<int:id>', methods=['DELETE'])
@cross_origin() # allow all origins all methods.
def remove_course():
    response = ManagerController.delete_manager(id)
    return jsonify({"message" : response})

@app.errorhandler(404)
def route_not_found(error):
    return  not_found("Route does not exist")



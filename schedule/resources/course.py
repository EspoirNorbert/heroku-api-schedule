from flask import jsonify,make_response
from sqlalchemy.exc import SQLAlchemyError
from schedule.models import *

class CourseController():

    def get_all_courses():
        courses = db.session.query(Course,Classroom,Teacher,Room,Subject).filter(Course.classroom_id==Classroom.id,Course.teacher_id==Teacher.id,Course.room_id==Room.id,Course.subject_id==Subject.id).order_by(Course.id.desc()).all()
        return make_response(jsonify(courses= [ CourseController.json(course,classroom,teacher,room,subject) for course,classroom,teacher,room,subject in courses ] ,count=len(courses))),200 

    def get_total_course():
        total = Course.query.count()
        return make_response(jsonify(total_course=total)),200
    
    def get_teacher(teacher_id):
        teacher = db.session.query(Teacher,User).select_from(Teacher).join(User).filter(Teacher.id==teacher_id).first() 
        return {'teacher':{'grade': teacher.Teacher.grade,'firstname': teacher.User.firstname,'lastname':teacher.User.lastname}}

    def json(course,classroom,teacher,room,subject):
        return {"id" : course.id,"classroom" : classroom.name,"room" : room.name,"teacher": CourseController.get_teacher(teacher.id),"subject": subject.name,"date":course.date,"start_hour": course.start_hour,"end_hour": course.end_hour}
    
    def add_course(request):
        try:
            data = request.get_json(force=True)
            #get data from api
            teacher = data['teacher']
            classroom = data['classroom']
            room = data['room']
            subject = data['subject']
            date = data['date']
            start_hour = data['start_hour']
            end_hour = data['end_hour']
            #check if teacher exist
            existing_teacher = Teacher.query.join(User).filter(User.firstname.__eq__(teacher)).first()
            print(existing_teacher.grade)
            #check if classroom exist
            existing_classroom  = Classroom.query.filter(Classroom.name.__eq__(classroom)).first()
            print(existing_classroom.name)
            #check if room exist
            existing_room    = Room.query.filter(Room.name.__eq__(room)).first()
            print(existing_room.name)
            #check if subject exist
            existing_subject = Subject.query.filter(Subject.name.__eq__(subject)).first()
            print(existing_subject.name)

            if existing_classroom and existing_teacher and existing_room and existing_subject:
                try:
                    new_course = Course(teacher_id=existing_teacher.id,classroom_id=existing_classroom.id,subject_id=existing_subject.id,room_id=existing_room.id,date=date,start_hour=start_hour,end_hour=end_hour)
                    db.session.add(new_course)
                    db.session.commit()
                    return make_response(jsonify(status='success', message='course created successfully' )),201 
                except Exception as e:
                    db.session.rollback()
                    return make_response(jsonify(status='failed', message=str(e))),401 
            else:
                return make_response(jsonify(status='failed', message="classroom, teacher,room and subject doesn't exist")),404      
        except SQLAlchemyError as e:
               return make_response(jsonify(message= str(e))),500
            
    def get_course(_id):
        try:
            course = db.session.query(Course,Classroom,Teacher,Room,Subject).filter(Course.classroom_id==Classroom.id,Course.teacher_id==Teacher.id,Course.room_id==Room.id,Course.subject_id==Subject.id).filter(Course.id ==_id).first()
            if course:
                return make_response(jsonify(course=CourseController.json(course.Course,course.Classroom,course.Teacher,course.Room,course.Subject))),200 
            else:
                return make_response(jsonify(message="course dont exists", status="failed")),401
        except SQLAlchemyError as e:
            return make_response(jsonify(message= str(e))),500
    
    def get_course_by_classroom(classroom):
        try:
            existing_classroom  = Classroom.query.filter(Classroom.name.__eq__(classroom)).first()
            if existing_classroom:
               courses = db.session.query(Course,Classroom,Teacher,Room,Subject).filter(Course.classroom_id==Classroom.id,Course.teacher_id==Teacher.id,Course.room_id==Room.id,Course.subject_id==Subject.id).filter(Classroom.name == classroom).all()
               return make_response(jsonify(courses= [ CourseController.json(course,classroom,teacher,room,subject) for course,classroom,teacher,room,subject in courses ] ,count=len(courses), classroom=classroom)),200 
            else:
                return make_response(jsonify(message="classroom dont exists", status="failed")),401
        except SQLAlchemyError as e:
            return make_response(jsonify(message= str(e))),500
    
    def get_course_by_week(classroom,start,end):
        try:
            #existing classroom
            existing_classroom  = Classroom.query.filter(Classroom.name.__eq__(classroom)).first()
            if existing_classroom:
                courses = db.session.query(Course,Classroom,Teacher,Room,Subject). \
                filter(Course.classroom_id==Classroom.id). \
                filter(Course.teacher_id==Teacher.id). \
                filter(Course.room_id==Room.id). \
                filter(Course.subject_id==Subject.id). \
                filter(Classroom.name == existing_classroom.name). \
                filter(Course.date.between(start,end)). \
                all()
                return make_response(jsonify(
                    courses=[CourseController.json(course,classroom,teacher,room,subject) for course,classroom,teacher,room,subject in courses],
                    count=len(courses),periode={"from" : start, "to" : end}
                    )),200 
            else:
                return make_response(jsonify(message="classroom dont exists", status="failed")),401
        except SQLAlchemyError as e:
            return make_response(jsonify(message= str(e))),500
    
    def update_course(request):
        return make_response(jsonify(message= 'course updated successfully',status='success')),200

    def delete_course(request):
        return make_response(jsonify(message= 'course deleted successfully' , status='success')),200
        
 
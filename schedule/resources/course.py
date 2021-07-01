from schedule.models import *


class CourseController():

    def get_all_course():
        results = db.session.query(Course,Classroom,Teacher,Room,Subject).filter(Course.classroom_id==Classroom.id,Course.teacher_id==Teacher.id,Course.room_id==Room.id,Course.subject_id==Subject.id).order_by(Course.id.desc()).all()
        return [ CourseController.json(course,classroom,teacher,room,subject) for course,classroom,teacher,room,subject in results ]
    
    def json(course,classroom,teacher,room,subject):
        return {
        "course_id" : course.id,
        "classe" : classroom.name,
        "room" : room.name,
        "teacher": {
            "grade": teacher.grade,
            "firstname":User.query.join(Teacher).filter(Teacher.id==teacher.id).first().firstname,
            "lastname":User.query.join(Teacher).filter(Teacher.id==teacher.id).first().lastname
            },
        "subject": subject.name,
        "date":course.date,
        "start_hour": course.start_hour,
        "end_hour": course.end_hour
        }
        
    def add_course(request):
        #create room 
        classroom = request['classroom']
        teacher = request['teacher']
        room = request['room']
        subject = request['subject']
        date = request['date']
        start_hour = request['start_hour']
        end_hour = request['end_hour']

        #check 
        existing_classe  = Classroom.query.filter_by(name=classroom).first()
        existing_teacher = Teacher.query.join(User).filter(User.firstname.__eq__(teacher)).first()
        existing_room    = Room.query.filter_by(name=room).first()
        existing_subject = Subject.query.filter_by(name=subject).first()
        
        if existing_classe and existing_teacher and existing_room and existing_subject:
           #create course 
           course = Course(existing_teacher.id,existing_classe.id,existing_room.id,existing_subject.id,date,start_hour,end_hour)
           #creta
           db.session.add(course)
           db.session.commit()
           return "Course successful added !"
        else:
            return {"error" : "classe or teacher or room or subject no found" }
        
    def get_course(_id):
        existing_id = Course.query.filter_by(id=_id).first()
        if existing_id is None:
             return "id n'existe pas dans la base de donnee"
        else:
            results = db.session.query(Course,Classroom,Teacher,Room,Subject).filter(Course.classroom_id==Classroom.id,Course.teacher_id==Teacher.id,Course.room_id==Room.id,Course.subject_id==Subject.id).filter(Course.id ==_id).first()
            return {
            "course_id" : results.Course.id,
            "classe" : results.Classroom.name,
            "room" : results.Room.name,
            "teacher": {
                "grade": results.Teacher.grade,
                "firstname":User.query.join(Teacher).filter(Teacher.id==results.Teacher.id).first().firstname,
                "lastname":User.query.join(Teacher).filter(Teacher.id==results.Teacher.id).first().lastname
            },
            "subject": results.Subject.name,
            "date":results.Course.date,
            "start_hour":results.Course.start_hour,
             "end_hour": results.Course.end_hour
            } 
    
    def get_course_by_class(classroom):
        #check existing classroom
        existing_classroom = Classroom.query.filter_by(name=classroom).first()
        
        #check if classroom exist
        if existing_classroom is None:
             return "Cette classe n'existe pas dans la base de donnee"
        else:
            results = db.session.query(Course,Classroom,Teacher,Room,Subject).filter(Course.classroom_id==Classroom.id,Course.teacher_id==Teacher.id,Course.room_id==Room.id,Course.subject_id==Subject.id).filter(Classroom.name == classroom).all()
            return [ CourseController.json(course,classroom,teacher,room,subject) for course,classroom,teacher,room,subject in results ]
    
    def get_course_by_week(classroom,start,end):
        #check existing classroom
        #existing_start_date = Course.query.filter_by(date=start).first()
        #existing_end_date  =  Course.query.filter_by(date=end).first()
        existing_classroom  = Classroom.query.filter_by(name=classroom).first()

        if existing_classroom:
            results = db.session.query(Course,Classroom,Teacher,Room,Subject). \
            filter(Course.classroom_id==Classroom.id). \
            filter(Course.teacher_id==Teacher.id). \
            filter(Course.room_id==Room.id). \
            filter(Course.subject_id==Subject.id). \
            filter(Classroom.name == existing_classroom.name). \
            filter(Course.date.between(start ,end)). \
            all()
            return [ CourseController.json(course,classroom,teacher,room,subject) for course,classroom,teacher,room,subject in results ]
        else:
            return "Cette Periode et cette classe n'existe pas dans la base de donnee"

    def get_total_course():
        """ Get total Rooms """
        return Course.query.count()
    
    def get_course_by_period(classroom):
        #recuperer les cours
        #les trier par periode et les renvoyer
        periods_course = []

    def update_course(_id):
        pass

    def delete_course(_id):
        pass

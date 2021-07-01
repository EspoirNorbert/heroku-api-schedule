from schedule.models import *
from  werkzeug.security import generate_password_hash


class TeacherController():

    def get_all_teacher():
        """Get all Teachers from database"""
        results = db.session.query(User,Teacher). \
            select_from(User).join(Teacher).order_by(Teacher.id.desc()).all()
        return[TeacherController.json(teacher,user) for user,teacher in results]
    
    def get_total_teacher():
        """Get total Teacher """
        return Teacher.query.count()

    def json(teacher,user):
        """return json format"""
        return {
            'teacher_id':teacher.id, 
            'grade':teacher.grade,
            'lastname':user.lastname,
            'firstname':user.firstname,
            'email': user.email,
            "gender":user.gender,
            "subjects": [ subject.name for subject in Subject.query.join(Teacher).filter(Teacher.id==teacher.id).all()]
            }
    
    def add_teacher(request):
        """Add Teacher in databases """
        #recuperer le json
        firstname = request['firstname']
        lastname = request['lastname']
        email = request['email']
        gender = request['gender']
        password = request['password']
        grade = request['grade']

        hash_passwod = generate_password_hash(password)

        #creer le utilisateur
        new_user = User(lastname, firstname, email, gender, hash_passwod, "enseignant")
        db.session.add(new_user) 
        db.session.commit()
        new_Teacher = Teacher(grade,new_user.id)
        db.session.add(new_Teacher)
        db.session.commit()
        return "Enseignant ajouté avec success"
    
    def get_teacher(_id):
        #retrieve id 
        existing_id = Teacher.query.filter_by(id=_id).first()
        #condition
        if existing_id is None:
             return "id n'existe pas dans la base de donnee"
        else:
            results = db.session.query(User,Teacher).\
            select_from(User).join(Teacher).filter(Teacher.id ==_id).first()
            return {
            'teacher_id':results.Teacher.id, 
            'grade': results.Teacher.grade,
            'lastname':results.User.lastname,
            'firstname':results.User.firstname,
            'email': results.User.email,
            'gender':results.User.gender
            }   

    def update_teacher(_id):
        pass
    
    def delete_teacher(_id):
        pass
        




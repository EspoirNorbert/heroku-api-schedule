from schedule.models import *
from  werkzeug.security import generate_password_hash

class StudentController():

    def get_all_student():
        """Get all students from database"""
        results = db.session.query(User,Student,Classroom). \
            select_from(User).join(Student).join(Classroom).order_by(Student.id.desc()).all()
        return [StudentController.json(student,user,classroom) for user,student,classroom in results]
   
    def get_total_student():
        """Get total student """
        return Student.query.count()

    def json(student,user,classroom):
        """return json format"""
        return {
            'student_id':student.id, 
            'number_id': student.id_number,
            'lastname':user.lastname,
            'firstname':user.firstname,
            'email': user.email,
            "gender":user.gender,
            "classroom": classroom.name
            }
    
    def add_student(request):
        """Add student in databases """
        #recuperer le json
        firstname = request['firstname']
        lastname = request['lastname']
        email = request['email']
        gender = request['gender']
        password = request['password']
        id_number = request['id_number']
        classrom = request['classrom'] 

        #found classroom
        existing_classe = Classroom.query.filter_by(name=classrom).first()

        #si la classe n'exitse
        if existing_classe is None:
            return "Cette classe n'existe pas dans la base de donnee"
        else:
            hash_passwod = generate_password_hash(password)
            #creer le utilisateur
            new_user = User(lastname, firstname, email, gender, hash_passwod, "etudiant")
            db.session.add(new_user) 
            db.session.commit()
            new_student = Student(id_number,existing_classe.id,new_user.id)
            db.session.add(new_student)
            db.session.commit()
            return "Etudiant ajouté avec success"
    
    def get_student(_id):
        #retrieve id 
        existing_id = Student.query.filter_by(id=_id).first()
        #condition
        if existing_id is None:
             return {'message':'student not found'},404
        else:
            results = db.session.query(User,Student,Classroom).\
            select_from(User).join(Student).join(Classroom).filter(Student.id ==_id).first()
            return {
                "student_id" :  results.Student.id,
                "number_id" :  results.Student.id_number,
                "lastname"   :  results.User.lastname,
                "firstname"  :  results.User.firstname,
                "email"      :  results.User.email,
                "gender"     :  results.User.gender,
                "classroom"  :  results.Classroom.name
            }

    def update_student(_id):
        pass
    
    def delete_student(_id):
        pass
        




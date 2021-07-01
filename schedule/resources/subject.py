from schedule.models import *

class SubjectController():

    def get_all_subject():
        """Get all Subjects from database"""
        results = db.session.query(Subject,Teacher,User). \
            select_from(Subject).join(Teacher).join(User).order_by(Subject.id.desc()).all()
        return [SubjectController.json(subject,teacher,user) for subject,teacher,user in results]
    
    def get_total_subject():
        """Get total Subject """
        return Subject.query.count()

    def json(subject,teacher,user):
        """return json format"""
        return {
            "subject_id":  subject.id,
            "name"        :subject.name,
            "coefficient" :subject.coefficient,
            "teacher"     :  {
                "lastname"    : user.lastname,
                "firstname"   : user.firstname,
                "grade"       : teacher.grade
             } 
            }
    
    def add_subject(request):
        """Add Subject in databases """
        #recuperer le json
        name = request['name']
        coefficient = request['coefficient']
        teacher = request['teacher']
        #found Subject
        existing_teacher = Teacher.query.join(User).filter(User.firstname.__eq__(teacher)).first()

        #si la classe n'exitse
        if existing_teacher is None:
            return "Cette enseignant n'existe pas dans la base de donnee"
        else:
            #creer le utilisateur
            new_subject = Subject(name,coefficient,existing_teacher.id)
            db.session.add(new_subject) 
            db.session.commit()
            return "Matiere ajouté avec success"
    
    def get_subject(_id):
        #retrieve id 
        existing_id = Subject.query.filter_by(id=_id).first()
        #condition
        if existing_id is None:
             return "id n'existe pas dans la base de donnee"
        else:
            results = db.session.query(Subject,Teacher,User). \
            select_from(Subject).join(Teacher).join(User).filter(Subject.id ==_id).first()
            return {
            "Subject_id"  :  results.Subject.id,
            "name"        :  results.Subject.name,
            "coefficient" :  results.Subject.coefficient,
            "Teacher"     :  {
                "lastname"    : results.User.lastname,
                "firstname"   : results.User.firstname,
                "title"       : results.Teacher.grade
             } 
            }   

    def update_subject(_id):
        pass
    
    def delete_subject(_id):
        pass
        




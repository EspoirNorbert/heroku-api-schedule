from schedule.models import *


class ClassroomController():

    def get_all_classroom():
        """Get all Classrooms from database"""
        results = db.session.query(Classroom,Manager,User). \
            select_from(Classroom).join(Manager).join(User).order_by(Classroom.id.desc()).all()
        return [ClassroomController.json(classroom,manager,user) for classroom,manager,user in results]
    
    def get_total_classroom():
        """Get total Classroom """
        return Classroom.query.count()

    def json(classroom,manager,user):
        """return json format"""
        return {
            "classroom_id":  classroom.id,
            "name"        :  classroom.name,
            "manager"     :  {
                "lastname"    : user.lastname,
                "firstname"   : user.firstname,
                "title":        manager.title
             } 
            }
    
    def add_classroom(request):
        """Add Classroom in databases """
        #recuperer le json
        name = request['name']
        manager = request['manager']
        #found classroom
        existing_manager = Manager.query.join(User).filter(User.firstname.__eq__(manager)).first()

        #si la classe n'exitse
        if existing_manager is None:
            return "Cette manager n'existe pas dans la base de donnee"
        else:
            #creer le utilisateur
            new_classroom = Classroom(name, existing_manager.id)
            db.session.add(new_classroom) 
            db.session.commit()
            return "Classe ajouté avec success"
    
    def get_classroom(_id):
        #retrieve id 
        existing_id = Classroom.query.filter_by(id=_id).first()
        #condition
        if existing_id is None:
             return "id n'existe pas dans la base de donnee"
        else:
            results = db.session.query(Classroom,Manager,User). \
            select_from(Classroom).join(Manager).join(User).filter(Classroom.id ==_id).first()
            return {
            "classroom_id":  results.Classroom.id,
            "name"        :  results.Classroom.name,
            "manager"     :  {
                "lastname"    : results.User.lastname,
                "firstname"   : results.User.firstname,
                "title":        results.Manager.title
             } 
            }   
    
    def update_classroom(_id):
        pass
    
    def delete_classroom(_id):
        pass
        



from schedule.models import *
from  werkzeug.security import generate_password_hash

class ManagerController():

    def get_all_manager():
        """Get all Managers from database"""
        results = db.session.query(Manager,User). \
            select_from(Manager).join(User).order_by(Manager.id.desc()).all()
        return [ManagerController.json(manager,user) for manager,user in results]
    
    def get_total_manager():
        """Get total Manager """
        return Manager.query.count()

    def json(manager,user):
        """return json format"""
        return {
            'manager_id':manager.id, 
            'title':manager.title,
            'lastname':user.lastname,
            'firstname':user.firstname,
            'email': user.email,
            "gender":user.gender,
            "classroom": [ classroom.name for classroom in Classroom.query.join(Manager).filter(Manager.id==manager.id).all()]
           }
    
    def add_manager(request):
        """Add Manager in databases """
        #recuperer le json
        firstname = request['firstname']
        lastname = request['lastname']
        email = request['email']
        gender = request['gender']
        password = request['password']
        title = request['title']

        hash_passwod = generate_password_hash(password)

        #creer le utilisateur
        new_user = User(lastname, firstname, email, gender, hash_passwod, "responsable")
        db.session.add(new_user) 
        db.session.commit()
        new_manager = Manager(title,new_user.id)
        db.session.add(new_manager)
        db.session.commit()
        return "Responsable ajouté avec success"
    
    def get_manager(_id):
        #retrieve id 
        existing_id = Manager.query.filter_by(id=_id).first()
        #condition
        if existing_id is None:
             return " id n'existe pas dans la base de donnee"
        else:
            results = db.session.query(User,Manager,Classroom).\
            select_from(User).join(Manager).join(Classroom).filter(Manager.id ==_id).first()
            return {
                "manager_id" :  results.Manager.id,
                'title'      :  results.Manager.title,
                "lastname"   :  results.User.lastname,
                "firstname"  :  results.User.firstname,
                "email"      :  results.User.email,
                "gender"     :  results.User.gender,
                "classroom"  :  [ classroom.name for classroom in Classroom.query.join(Manager).filter(Manager.id==results.Manager.id).all()]
            }   

    def update_manager(_id):
        pass
    
    def delete_manager(_id):
        pass
        
    




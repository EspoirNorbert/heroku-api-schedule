from schedule.models import *

class UserController():

    def login(request):
        pass

    def get_all_users():
        return [User.json(user) for user in User.query.order_by(User.id.desc()).all()]

    def get_user(_id):
        existing_id = User.query.filter_by(id=_id).first()

        if existing_id is None:
             return " id n'existe pas dans la base de donnee"
        else:
            return User.json(User.query.filter_by(id=_id).first())
    
    def get_total_user():
        """Get total Manager """
        return User.query.count()

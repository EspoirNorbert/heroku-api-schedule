from schedule.models import *

class RoomController():

    def get_all_rooms():
        return [Room.json(room) for room in Room.query.all()]
    
    def add_room(request):
        #create room 
        #recuperer le json
        name = request['name']
        capacity = request['capacity']
        
        #create room item
        new_room = Room(name,capacity)
        #add room
        db.session.add(new_room)
        #commit
        db.session.commit()
        #return message
        return "Salle ajouté avec success"

    def get_room(_id):
        return Room.json(Room.query.filter_by(id=_id).all())
    
    def get_total_room():
        """ Get total Rooms """
        return Room.query.count()

    def update_room(_id):
        pass
    
    def delete_room(_id):
        pass
        
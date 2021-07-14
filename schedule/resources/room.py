from flask import jsonify,make_response
from sqlalchemy.exc import SQLAlchemyError
from schedule.models import *

class RoomController():

    def get_all_room():
        rooms = Room.query.all()
        return make_response(jsonify(rooms= [RoomController.json(room) for room in rooms] ,count=len(rooms))),200 

    def get_total_room():
        total = Room.query.count()
        return make_response(jsonify(total_room=total)),200

    def json(room):
        return {'id':room.id,'name':room.name,'capacity':room.capacity}
 
    def add_room(request):
        try:
            data = request.get_json(force=True)
            #get data from api
            name = data['name']
            capacity = data['capacity']
            #check if room exist
            existing_room = Room.query.filter(Room.name.__eq__(name)).first()
            if existing_room is None:
                try:
                    new_room = Room(name=name, capacity=capacity)
                    db.session.add(new_room) 
                    db.session.commit()
                    return make_response(jsonify(status='success', message='room created successfully' )),401 
                except Exception as e:
                    db.session.rollback()
                    return make_response(jsonify(status='failed', message=str(e))),401     
            else:
               return make_response(jsonify(message='room already exist', status='failed')),202
        except SQLAlchemyError as e:
               return make_response(jsonify(message= str(e))),500
            
    def get_room(room_id):
        try:
            room = Room.query.filter_by(id=room_id).first()
            if room:
                return make_response(jsonify(room= RoomController.json(room))),200 
            else:
                return make_response(jsonify(message="room dont exists", status="failed")),401
        except SQLAlchemyError as e:
            return make_response(jsonify(message= str(e))),500
    
    def update_room(request):
        return make_response(jsonify(message= 'room updated successfully',status='success')),200

    def delete_room(request):
        return make_response(jsonify(message= 'room deleted successfully' , status='success')),200
        





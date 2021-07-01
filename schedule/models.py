from flask_sqlalchemy import SQLAlchemy

# Create database connection object
db = SQLAlchemy()


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lastname = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)

    def __init__(self, lastname, firstname, email, gender, password, type):
        self.lastname = lastname
        self.firstname = firstname
        self.email = email
        self.gender = gender
        self.password = password
        self.type = type

    def __repr__(self):
        return '<User %r>' % self.lastname
    
    def json(self):
        return {
            'id': self.id,
            'lastname'  :  self.lastname,
            'firstname' :  self.firstname,
            'email'     :  self.email,
            'gender'    :  self.gender,
            'password'  :  self.password,
            'type'      :  self.type,
        }
 
class Manager(db.Model):

    __tablename__ = 'managers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
     
    def __init__(self, title, user_id):
        self.title = title
        self.user_id=user_id
        
    def __repr__(self):
        return '<Manager %r>' % self.title

class Classroom(db.Model):

    __tablename__ = 'classrooms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
      
    def __init__(self, name, manager_id):
        self.name = name,
        self.manager_id = manager_id
    
    def __repr__(self):
        return '<Classroom %r>' % self.name
    
class Student(db.Model):

    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_number = db.Column(db.Integer, unique=True, nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, id_number, classroom_id, user_id):
        self.id_number = id_number
        self.classroom_id = classroom_id
        self.user_id = user_id
    
    def __repr__(self):
        return '<Student %r>' % self.id_number

class Teacher(db.Model):

    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, grade, user_id):
        self.grade = grade,
        self.user_id = user_id
    
    def __repr__(self):
        return '<Teacher %r>' % self.grade

class Subject(db.Model):

    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    coefficient = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)

    def __init__(self, name, coefficient, teacher_id):
        self.name = name
        self.coefficient = coefficient
        self.teacher_id = teacher_id

    def __repr__(self):
        return '<Subject %r>' % self.name

class Room(db.Model):

    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
    
    def __repr__(self):
        return '<Room %r>' % self.name
    
    def json(self):
        return {
            'id': self.id,
            'name'  :  self.name,
            'capacity' :  self.capacity
        }

class Course(db.Model):

    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    date = db.Column(db.String(), nullable=False)
    start_hour = db.Column(db.String(80), nullable=False)
    end_hour = db.Column(db.String(80), nullable=False)

    def __init__(self, teacher_id, classroom_id, room_id, subject_id, date, start_hour, end_hour):
        self.teacher_id = teacher_id
        self.classroom_id = classroom_id
        self.room_id = room_id
        self.subject_id = subject_id
        self.date = date
        self.start_hour = start_hour
        self.end_hour = end_hour

    def __repr__(self):
        return '<Course %r>' % self.date











 




    







    


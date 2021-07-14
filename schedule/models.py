from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    gender = db.Column(db.String(2), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    type = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.lastname
    
class Manager(db.Model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
   
    def __repr__(self):
        return '<Manager %r>' % self.title

class Classroom(db.Model):

    __tablename__ = 'classrooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))

    def __repr__(self):
        return '<Classroom %r>' % self.name
    
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    id_number = db.Column(db.String(80), unique=True, nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classrooms.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return '<Student %r>' % self.id_number

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return '<Teacher %r>' % self.grade

class Subject(db.Model):

    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    coefficient = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)

    def __repr__(self):
        return '<Subject %r>' % self.name

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Room %r>' % self.name
    
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

    def __repr__(self):
        return '<Course %r>'% self.date

class Developper(db.Model):
    __tablename__ = 'developpers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(80), unique=True)
    api_key = db.Column(db.String(300))
    password = db.Column(db.String(250))

    def __repr__(self):
        return '<Developper %r>' % self.name
    











 




    







    


from schedule.views import app
from schedule.models import db

with app.app_context():
    db.drop_all()
    db.create_all()
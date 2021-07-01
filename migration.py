from schedule.views import app
from schedule.models import db

with app.app_context():
    db.create_all()
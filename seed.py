from models import User, db
from app import app

db.drop_all()
db.create_all()

joel = User(fname='Joel', lname='Burton', img_url="http://joelburton.com/joel-burton.jpg")
tom = User(fname='Tom', lname='Frommyspace')

db.session.add(joel)
db.session.add(tom)

db.session.commit()
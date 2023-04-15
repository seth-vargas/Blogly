""" Seed file to make sample data for users db """

from models import User, db, Post, datetime
from app import app

def seed():

    # Create all tables
    db.drop_all()
    db.create_all()

    # Add users        
    u1 = User(first_name="John",
            last_name="Doe",
            image_url="https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8dXNlciUyMHByb2ZpbGV8ZW58MHx8MHx8&w=1000&q=80")
    u2 = User(first_name="Jane",
            last_name="Doe",
            image_url="https://pixinvent.com/materialize-material-design-admin-template/app-assets/images/user/12.jpg")
    u3 = User(first_name="Timmy",
            last_name="Smith")

    p1 = Post(title="My First Post", content="oh, Hai", created_at=datetime.now(), user_id=1)

    # add and commit users to db
    db.session.add_all([u1, u2, u3])
    db.session.commit()

    db.session.add(p1)
    db.session.commit()

# Runs ONLY if seed.py is called, NOT when imported from other files
if __name__ == '__main__':
    seed()
from app import app
from models import db, User

def run_seeds():
    print('Seeding database ... 🌱')
    # Add your seed data here
    with app.app_context():
      user1 = User('rmdashrfv2', 'michael2@example.com', '111111111')
      user1 = User('rmdashrfv2', 'michael2@example.com', '111111111')
      user1 = User('rmdashrfv2', 'michael2@example.com', '111111111')
      user1 = User('rmdashrfv2', 'michael2@example.com', '111111111')
      user1 = User('rmdashrfv2', 'michael2@example.com', '111111111')
      db.session.add_all([user1])
      db.session.commit()
      print('Done! 🌳')

run_seeds()
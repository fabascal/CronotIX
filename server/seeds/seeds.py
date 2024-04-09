from flask_seeder import Seeder
from website.auth.models import User


def create_user_admin(self):
    print("inicia usuario")
    admin = User(username="Administrador", email='admin@mail.com', plaintext_password='1234')
    self.db.session.add(admin)
    self.db.session.commit()
    
    
class UserSeeder(Seeder):
    def run(self):
        create_user_admin(self)
from flask_seeder import Seeder
from website.auth.models import User
from website.home.models import AssistantsVersion, AssistantsModels
from website.home.utils.keyUtils import GenerateUUIDStyled


def create_user_admin(self):
    print("inicia usuario")
    admin = User(username="Administrador", email='admin@mail.com', plaintext_password='1234')
    self.db.session.add(admin)
    self.db.session.commit()
    
def create_assistant_version(self):
    print("inicia version")
    versions_list = ["Individualizado", ]
    for version in versions_list:
        assistant_version = AssistantsVersion(name=version)
        self.db.session.add(assistant_version)
    self.db.session.commit()
    
def create_models(self):
    print("inicia modelos")
    models_list = [
        {"model": "OA-3.5"},
        {"model": "OA-4.0"}
    ]
    for model_data in models_list:
        try:
            print(f'model: {model_data}')
            model = AssistantsModels(id=GenerateUUIDStyled('mdls'), name=model_data["model"])
            print(f'Generated ID: {model.id}')
            self.db.session.add(model)
            self.db.session.commit()
        except Exception as e:
            print(f"Error al insertar el modelo: {e}")
            self.db.session.rollback()
    
    
class UserSeeder(Seeder):
    def run(self):
        create_user_admin(self)
        create_models(self)
        create_assistant_version(self)
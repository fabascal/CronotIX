from website import db
from sqlalchemy.dialects.postgresql import JSON  # Import específico para JSON en PostgreSQL
from sqlalchemy.types import JSON as JSONType  # Import genérico para compatibilidad
from website.home.utils.keyUtils import GenerateUUIDStyled

class AssistantsModels(db.Model):
    __tablename__ = 'assistantsmodels'
    id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: GenerateUUIDStyled('mdls'), primary_key=True)
    name = db.Column(db.String(100), unique=False)
    oa_name = db.Column(db.String(100), unique=False)
    active = db.Column(db.Boolean, default=True)
    assistants = db.relationship("Assistants", back_populates="model")  # Relación one-to-many con Assistants
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '<Model %r>' % self.id
    

class Assistants(db.Model):
    __tablename__ = 'assistants'
    id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: GenerateUUIDStyled('asst'), primary_key=True)
    id_openai = db.Column(db.String(36), unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True) # Relación one-to-many con User o Cliente
    user = db.relationship('User', back_populates='assistants')  # Relación one-to-many con User
    name = db.Column(db.String(100), unique=False)
    description = db.Column(db.String(100), unique=False)
    instructions = db.Column(db.String(1000), unique=False)
    model_id = db.Column(db.String(36), db.ForeignKey('assistantsmodels.id'), nullable=False, index=True)
    model = db.relationship('AssistantsModels', back_populates='assistants')  # Relación one-to-many con Models
    functions = db.relationship("AssistantsFunctions", back_populates="assistantF", lazy='dynamic')  # Relación one-to-many con AssistantsFunctions
    version_id = db.Column(db.String(36), db.ForeignKey('assistantsversion.id'), nullable=False, index=True)
    version = db.relationship('AssistantsVersion', back_populates='assistants')  # Relación one-to-many con AssistantsVersion
    apikey = db.relationship("AssistantsApiKey", back_populates="assistantA", uselist=False)  # Relación one-to-one con AssistantsApiKey
    vector = db.relationship("AssistantsVector", back_populates="assistant", uselist=False)  # Relación one-to-one con AssistantsVector
    file = db.relationship("AssistantsFiles", back_populates="assistant", lazy='dynamic')  # Relación one-to-many con AssistantsFiles
    avatar_path = db.Column(db.String(100), unique=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '<Assistants %r>' % self.id

class AssistantsFunctions(db.Model):
    __tablename__ = 'assistantsfunctions'
    id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: GenerateUUIDStyled('fncs'), primary_key=True)
    description = db.Column(db.String(100), unique=False)
    parameters = db.Column(JSONType, nullable=False)
    assistant_id = db.Column(db.String(36), db.ForeignKey('assistants.id'), nullable=False)
    assistantF = db.relationship('Assistants', back_populates="functions")  # Relación many-to-one con Assistants
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '<Function %r>' % self.id
    
class AssistantsApiKey(db.Model):
    __tablename__ = 'assistantsapikey'
    id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: GenerateUUIDStyled('apky'), primary_key=True)
    apikey = db.Column(db.String(36), unique=True, nullable=False)
    assistant_id = db.Column(db.String(36), db.ForeignKey('assistants.id'), nullable=False, unique=True)
    assistantA = db.relationship("Assistants", back_populates="apikey")  # Relación one-to-one con Assistants
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
class AssistantsVersion(db.Model):
    __tablename__ = 'assistantsversion'
    id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: GenerateUUIDStyled('vers'), primary_key=True)
    name = db.Column(db.String(100), unique=False)
    assistants = db.relationship("Assistants", back_populates="version")  # Relación one-to-many con Assistants
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
class AssistantsVector(db.Model):
    __tablename__ = 'assistantsvector'
    id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: GenerateUUIDStyled('vect'), primary_key=True)
    vector = db.Column(db.String, nullable=True)
    assistant_id = db.Column(db.String(36), db.ForeignKey('assistants.id'), nullable=False, unique=True)
    assistant = db.relationship("Assistants", back_populates="vector")  # Relación one-to-one con Assistants
    files = db.relationship("AssistantsFiles", back_populates="vector", lazy='dynamic')  # Relación one-to-many con AssistantsFiles
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
class AssistantsFiles(db.Model):
    __tablename__ = 'assistantsfiles'
    id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: GenerateUUIDStyled('file'), primary_key=True)
    name = db.Column(db.String(100), unique=False)
    type = db.Column(db.String(50), unique=False)
    size = db.Column(db.String(50), unique=False)
    path = db.Column(db.String(100), unique=False)
    upload = db.Column(db.Boolean, default=False)
    vector_id = db.Column(db.String(36), db.ForeignKey('assistantsvector.id'), nullable=True)  # Clave foránea hacia AssistantsVector
    vector = db.relationship("AssistantsVector", back_populates="files")  # Relación one-to-many con AssistantsVector
    assistant_id = db.Column(db.String(36), db.ForeignKey('assistants.id'), nullable=True)  # Clave foránea hacia Assistants
    assistant = db.relationship("Assistants", back_populates="file")  # Relación one-to-many con Assistants
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    

from website import db
from website.utils.utils import get_uuid4
from sqlalchemy.dialects.postgresql import JSON  # Import específico para JSON en PostgreSQL
from sqlalchemy.types import JSON as JSONType  # Import genérico para compatibilidad

class Models(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    id_external = db.Column(db.String(36), unique=True, nullable=False, default=get_uuid4)
    name = db.Column(db.String(100), unique=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    def __repr__(self):
        return '<Model %r>' % self.id
    

class Assistants(db.Model):
    __tablename__ = 'assistants'
    id = db.Column(db.Integer, primary_key=True)
    id_external = db.Column(db.String(36), unique=True, nullable=False, default=get_uuid4)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), unique=False)
    instructions = db.Column(db.String(1000), unique=False)
    model_id = db.Column(db.String(36), db.ForeignKey('models.id'), nullable=False)
    function_id = db.Column(db.String(36), db.ForeignKey('assistantsfunctions.id'), nullable=False, unique=True)
    function = db.relationship("AssistantsFunctions", back_populates="assistant", uselist=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    def __repr__(self):
        return '<Assistant %r>' % self.id
    
class AssistantsFunctions(db.Model):
    __tablename__ = 'assistantsfunctions'
    id = db.Column(db.Integer, primary_key=True)
    id_external = db.Column(db.String(36), unique=True, nullable=False, default=get_uuid4)
    description  = db.Column(db.String(100), unique=False)
    parameters = db.Column(JSONType, nullable=False)
    assistant = db.relationship('Assistants', backref=db.backref('assistantsfunctions', uselist=False), uselist=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    def __repr__(self):
        return '<Function %r>' % self.id
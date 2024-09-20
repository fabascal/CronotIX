"""empty message

Revision ID: 5eadcc533da2
Revises: 
Create Date: 2024-09-11 22:37:45.808291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5eadcc533da2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assistantsmodels',
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('oa_name', sa.String(length=100), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('assistantsversion',
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('customer', sa.Boolean(), nullable=True),
    sa.Column('image_path', sa.String(length=120), nullable=False),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('assistants',
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('id_openai', sa.String(length=60), nullable=False),
    sa.Column('user_id', sa.String(length=60), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.String(length=300), nullable=True),
    sa.Column('instructions', sa.String(length=1000), nullable=True),
    sa.Column('model_id', sa.String(length=60), nullable=False),
    sa.Column('version_id', sa.String(length=60), nullable=False),
    sa.Column('avatar_path', sa.String(length=100), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['model_id'], ['assistantsmodels.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['version_id'], ['assistantsversion.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('id_openai')
    )
    with op.batch_alter_table('assistants', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_assistants_model_id'), ['model_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_assistants_user_id'), ['user_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_assistants_version_id'), ['version_id'], unique=False)

    op.create_table('assistantsapikey',
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('apikey', sa.String(length=60), nullable=False),
    sa.Column('assistant_id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['assistant_id'], ['assistants.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('apikey'),
    sa.UniqueConstraint('assistant_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('assistantsfunctions',
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.Column('parameters', sa.JSON(), nullable=False),
    sa.Column('assistant_id', sa.String(length=60), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['assistant_id'], ['assistants.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('assistantsvector',
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('vector', sa.String(), nullable=True),
    sa.Column('assistant_id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['assistant_id'], ['assistants.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('assistant_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('assistantsfiles',
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('file_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('size', sa.String(length=50), nullable=True),
    sa.Column('path', sa.String(length=100), nullable=True),
    sa.Column('upload', sa.Boolean(), nullable=True),
    sa.Column('vector_id', sa.String(length=60), nullable=True),
    sa.Column('assistant_id', sa.String(length=60), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.ForeignKeyConstraint(['assistant_id'], ['assistants.id'], ),
    sa.ForeignKeyConstraint(['vector_id'], ['assistantsvector.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('file_id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assistantsfiles')
    op.drop_table('assistantsvector')
    op.drop_table('assistantsfunctions')
    op.drop_table('assistantsapikey')
    with op.batch_alter_table('assistants', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_assistants_version_id'))
        batch_op.drop_index(batch_op.f('ix_assistants_user_id'))
        batch_op.drop_index(batch_op.f('ix_assistants_model_id'))

    op.drop_table('assistants')
    op.drop_table('users')
    op.drop_table('assistantsversion')
    op.drop_table('assistantsmodels')
    # ### end Alembic commands ###
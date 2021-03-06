"""Working teachers, ratings, users table

Revision ID: 1e9412162ad4
Revises: 
Create Date: 2019-08-13 00:55:05.996793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e9412162ad4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('dept', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('access', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_dept'), 'user', ['dept'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('teacher',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=True),
    sa.Column('last_name', sa.String(length=64), nullable=True),
    sa.Column('dept', sa.String(length=64), nullable=True),
    sa.Column('overall_score', sa.Float(), nullable=True),
    sa.Column('dedication_score', sa.Float(), nullable=True),
    sa.Column('leniency_score', sa.Float(), nullable=True),
    sa.Column('marks_score', sa.Float(), nullable=True),
    sa.Column('teaching_score', sa.Float(), nullable=True),
    sa.Column('friendliness_score', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teacher_created_at'), 'teacher', ['created_at'], unique=False)
    op.create_index(op.f('ix_teacher_dept'), 'teacher', ['dept'], unique=False)
    op.create_index(op.f('ix_teacher_first_name'), 'teacher', ['first_name'], unique=False)
    op.create_index(op.f('ix_teacher_last_name'), 'teacher', ['last_name'], unique=False)
    op.create_table('rating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('dedication_score', sa.Integer(), nullable=True),
    sa.Column('leniency_score', sa.Integer(), nullable=True),
    sa.Column('marks_score', sa.Integer(), nullable=True),
    sa.Column('teaching_score', sa.Integer(), nullable=True),
    sa.Column('friendliness_score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['teacher.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rating')
    op.drop_index(op.f('ix_teacher_last_name'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_first_name'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_dept'), table_name='teacher')
    op.drop_index(op.f('ix_teacher_created_at'), table_name='teacher')
    op.drop_table('teacher')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_dept'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###

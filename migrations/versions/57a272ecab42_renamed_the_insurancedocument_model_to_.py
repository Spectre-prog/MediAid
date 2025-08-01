"""Renamed the InsuranceDocument model to UserDocuments

Revision ID: 57a272ecab42
Revises: b2d7ec837d4c
Create Date: 2025-06-27 01:26:04.736418

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '57a272ecab42'
down_revision = 'b2d7ec837d4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=200), nullable=True),
    sa.Column('file_url', sa.String(length=500), nullable=True),
    sa.Column('upload_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('insurance_document')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('insurance_document',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('filename', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('file_url', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('upload_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('insurance_document_user_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('insurance_document_pkey'))
    )
    op.drop_table('user_document')
    # ### end Alembic commands ###

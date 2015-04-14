"""Add list and cards tables

Revision ID: 1c1883fada8
Revises: 18554c40c9e
Create Date: 2015-04-08 20:24:35.892248

"""

# revision identifiers, used by Alembic.
revision = '1c1883fada8'
down_revision = '18554c40c9e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.Column('modified_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.Column('name', sa.UnicodeText(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.Column('modified_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.Column('translation_id', sa.Integer(), nullable=False),
    sa.Column('list_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['list_id'], ['list.id'], ),
    sa.ForeignKeyConstraint(['translation_id'], ['translation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('card')
    op.drop_table('list')
    ### end Alembic commands ###

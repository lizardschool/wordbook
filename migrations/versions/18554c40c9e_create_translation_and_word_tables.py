"""Create translation and word tables.

Revision ID: 18554c40c9e
Revises:
Create Date: 2015-04-07 23:37:02.929894

"""

# revision identifiers, used by Alembic.
revision = '18554c40c9e'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'word',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('modified_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('language', sa.Enum('en', 'pl'), nullable=False),
        sa.Column('word', sa.UnicodeText(), nullable=False),
        sa.Column('ipa', sa.UnicodeText(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'translation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('modified_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('translation', sa.UnicodeText(), nullable=False),
        sa.Column('language', sa.Enum('en', 'pl'), nullable=False),
        sa.Column('word_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['word_id'], ['word.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('translation')
    op.drop_table('word')
    ### end Alembic commands ###

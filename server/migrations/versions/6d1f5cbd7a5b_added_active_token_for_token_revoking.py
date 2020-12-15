"""added active_token for token revoking

Revision ID: 6d1f5cbd7a5b
Revises: 2031f622a14d
Create Date: 2020-12-15 09:20:44.367962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d1f5cbd7a5b'
down_revision = '2031f622a14d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('active_token', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'active_token')
    # ### end Alembic commands ###

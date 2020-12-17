"""modified active_token -> active_token_iat for token revoking

Revision ID: 1b4fe88a45b5
Revises: 6d1f5cbd7a5b
Create Date: 2020-12-15 09:51:39.969618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b4fe88a45b5'
down_revision = '6d1f5cbd7a5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('active_token_iat', sa.Integer(), nullable=True))
    op.drop_column('users', 'active_token')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('active_token', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.drop_column('users', 'active_token_iat')
    # ### end Alembic commands ###
"""empty message

Revision ID: 3078f59d60f7
Revises: 4e5da17eb617
Create Date: 2024-03-17 14:59:13.713767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3078f59d60f7'
down_revision = '4e5da17eb617'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_name', sa.String(length=80), nullable=True))
        batch_op.drop_constraint('users_username_key', type_='unique')
        batch_op.create_unique_constraint(None, ['user_name'])
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_unique_constraint('users_username_key', ['username'])
        batch_op.drop_column('user_name')

    # ### end Alembic commands ###
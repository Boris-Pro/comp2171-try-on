"""empty message

Revision ID: 203c8cc3d9b9
Revises: 6b44ab4c0b25
Create Date: 2024-04-14 00:58:20.347945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '203c8cc3d9b9'
down_revision = '6b44ab4c0b25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.drop_column('items_to_view')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('items_to_view', sa.VARCHAR(length=200), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
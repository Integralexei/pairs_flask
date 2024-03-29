"""empty message

Revision ID: 363caffc63c2
Revises: 4e95a385ce48
Create Date: 2022-02-23 13:46:14.521581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '363caffc63c2'
down_revision = '4e95a385ce48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stocks')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stocks',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('ticker', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='stocks_pkey')
    )
    # ### end Alembic commands ###

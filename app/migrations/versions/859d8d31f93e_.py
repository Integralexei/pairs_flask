"""empty message

Revision ID: 859d8d31f93e
Revises: ccb5ec1f8dd3
Create Date: 2022-02-23 15:41:42.303937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '859d8d31f93e'
down_revision = 'ccb5ec1f8dd3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('symbols',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol_name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol_name', sa.String(length=50), nullable=False),
    sa.Column('price', sa.Numeric(precision=20, scale=4), nullable=False),
    sa.Column('symbol_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['symbol_id'], ['symbols.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prices')
    op.drop_table('symbols')
    # ### end Alembic commands ###

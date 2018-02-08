"""init

Revision ID: 0d3345bcc6c2
Revises: 
Create Date: 2018-02-08 17:38:38.656054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d3345bcc6c2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('return_code', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('ok', sa.Boolean(), nullable=False),
    sa.Column('host', sa.String(), nullable=True),
    sa.Column('start', sa.DateTime(), nullable=False),
    sa.Column('stop', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('stderr', sa.String(), nullable=True),
    sa.Column('stdout', sa.String(), nullable=True),
    sa.Column('command', sa.String(), nullable=True),
    sa.Column('server_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('log')
    # ### end Alembic commands ###

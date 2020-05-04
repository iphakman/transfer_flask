"""empty message

Revision ID: cbd6e4f53fe6
Revises: 
Create Date: 2020-05-03 22:34:28.969905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbd6e4f53fe6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('convertion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('currency', sa.String(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('iso_code', sa.String(length=3), nullable=True),
    sa.Column('fractional_unit', sa.String(), nullable=False),
    sa.Column('variance', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=False),
    sa.Column('phone_number', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(length=40), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('msdi', sa.String(length=50), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('destination', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_balance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('last_modified', sa.DateTime(), nullable=False),
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['transaction_id'], ['transaction.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_balance')
    op.drop_table('transaction')
    op.drop_table('users')
    op.drop_table('convertion')
    # ### end Alembic commands ###

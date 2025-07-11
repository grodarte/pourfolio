"""add Cocktail

Revision ID: 9225055cba58
Revises: 837a471d218c
Create Date: 2025-06-04 15:39:30.076297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9225055cba58'
down_revision = '837a471d218c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cocktails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ingredients', sa.String(), nullable=False),
    sa.Column('instructions', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('spirit_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['spirit_id'], ['spirits.id'], name=op.f('fk_cocktails_spirit_id_spirits')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_cocktails_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cocktails')
    # ### end Alembic commands ###

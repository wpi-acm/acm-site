"""Create officers table

Revision ID: 4fa893cdd432
Revises: 69cccb10f676
Create Date: 2024-03-22 13:54:39.037307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fa893cdd432'
down_revision = '69cccb10f676'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('acm_officers',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('term_start', sa.Date(), nullable=False),
    sa.Column('term_end', sa.Date(), nullable=True),
    sa.Column('position', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['acm_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('acm_officers')
    # ### end Alembic commands ###
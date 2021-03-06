"""empty message

Revision ID: e86e5f65a5a3
Revises: 1713fa18e6c6
Create Date: 2021-05-31 07:49:48.048152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e86e5f65a5a3'
down_revision = '1713fa18e6c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('word', table_name='vocabulary')
    op.create_unique_constraint('unique_word_translation', 'vocabulary', ['word', 'translation'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_word_translation', 'vocabulary', type_='unique')
    op.create_index('word', 'vocabulary', ['word'], unique=False)
    # ### end Alembic commands ###

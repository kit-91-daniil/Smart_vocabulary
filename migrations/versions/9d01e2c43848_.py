"""empty message

Revision ID: 9d01e2c43848
Revises: 
Create Date: 2020-06-20 13:21:42.758161

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9d01e2c43848'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('words')
    op.drop_table('interval_words')
    op.drop_index('login', table_name='users')
    op.drop_table('users')
    op.drop_index('word', table_name='vocabulary')
    op.drop_table('vocabulary')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vocabulary',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('word', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=40), nullable=True),
    sa.Column('translation', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=40), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('word', 'vocabulary', ['word'], unique=True)
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('login', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=60), nullable=False),
    sa.Column('name', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=40), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('login', 'users', ['login'], unique=True)
    op.create_table('interval_words',
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('word_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('addition_time', mysql.DATETIME(), nullable=False),
    sa.Column('repeating_time', mysql.DATETIME(), nullable=True),
    sa.Column('time_to_repeat', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='interval_words_ibfk_1'),
    sa.ForeignKeyConstraint(['word_id'], ['vocabulary.id'], name='interval_words_ibfk_2'),
    sa.PrimaryKeyConstraint('user_id', 'word_id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('words',
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('word_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='words_ibfk_1'),
    sa.ForeignKeyConstraint(['word_id'], ['vocabulary.id'], name='words_ibfk_2'),
    sa.PrimaryKeyConstraint('user_id', 'word_id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
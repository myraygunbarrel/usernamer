"""init_schema

Revision ID: 599d3fbae090
Revises: 
Create Date: 2020-02-24 18:41:34.277627

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

# revision identifiers, used by Alembic.
revision = '599d3fbae090'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
    sa.Column('updated_at', pg.TIMESTAMP(), server_default=sa.text('statement_timestamp()'),
              nullable=False, comment='Дата модификации'),
    sa.Column('created_at', pg.TIMESTAMP(), server_default=sa.text('statement_timestamp()'),
              nullable=False, comment='Дата создания'),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.VARCHAR(), nullable=False, comment='Имя'),
    sa.Column('last_name', sa.VARCHAR(), nullable=True, comment='Фамилия'),
    sa.Column('date_of_birth', pg.TIMESTAMP(), nullable=True, comment='Дата рождения'),
    sa.Column('date_fact', sa.VARCHAR(), nullable=True, comment='Интересный факт о дне рождения'),
    sa.Column('year_fact', sa.VARCHAR(), nullable=False, comment='Интересный факт о годе рождения'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('user')

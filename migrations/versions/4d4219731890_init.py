"""init

Revision ID: 4d4219731890
Revises: 9ad2c628bafe
Create Date: 2020-02-06 12:40:18.665073

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4d4219731890'
down_revision = '9ad2c628bafe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_roles_default', table_name='roles')
    op.drop_index('name', table_name='roles')
    op.drop_table('roles')
    op.add_column('user', sa.Column('role', sa.String(length=128), nullable=True))
    op.drop_constraint('user_ibfk_1', 'user', type_='foreignkey')
    op.drop_column('user', 'role_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('user_ibfk_1', 'user', 'roles', ['role_id'], ['id'])
    op.drop_column('user', 'role')
    op.create_table('roles',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=64), nullable=True),
    sa.Column('default', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('permissions', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.CheckConstraint('(`default` in (0,1))', name='roles_chk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('name', 'roles', ['name'], unique=True)
    op.create_index('ix_roles_default', 'roles', ['default'], unique=False)
    # ### end Alembic commands ###

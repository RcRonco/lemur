"""empty message

Revision ID: 3307381f3b88
Revises: 412b22cb656a
Create Date: 2016-05-20 17:33:04.360687

"""

# revision identifiers, used by Alembic.
revision = '3307381f3b88'
down_revision = '412b22cb656a'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text
from sqlalchemy.dialects import postgresql


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('authorities', 'owner',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.drop_column('authorities', 'not_after')
    op.drop_column('authorities', 'bits')
    op.drop_column('authorities', 'cn')
    op.drop_column('authorities', 'not_before')
    op.add_column('certificates', sa.Column('root_authority_id', sa.Integer(), nullable=True))
    op.alter_column('certificates', 'body',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('certificates', 'owner',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    op.drop_constraint(u'certificates_authority_id_fkey', 'certificates', type_='foreignkey')
    op.create_foreign_key(None, 'certificates', 'authorities', ['authority_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'certificates', 'authorities', ['root_authority_id'], ['id'], ondelete='CASCADE')
    ### end Alembic commands ###

    # link existing certificate to their authority certificates
    conn = op.get_bind()
    for id, body in conn.execute(text('select id, body from authorities')):
        # look up certificate by body, if duplications are found, pick one
        stmt = text('select id from certificates where body=:body')
        stmt = stmt.bindparams(body=body)
        root_certificate = conn.execute(stmt).fetchone()
        if root_certificate:
            stmt = text('update certificates set root_authority_id=:root_authority_id where id=:id')
            stmt = stmt.bindparams(root_authority_id=id, id=root_certificate[0])
            op.execute(stmt)


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'certificates', type_='foreignkey')
    op.drop_constraint(None, 'certificates', type_='foreignkey')
    op.create_foreign_key(u'certificates_authority_id_fkey', 'certificates', 'authorities', ['authority_id'], ['id'])
    op.alter_column('certificates', 'owner',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('certificates', 'body',
               existing_type=sa.TEXT(),
               nullable=True)
    op.drop_column('certificates', 'root_authority_id')
    op.add_column('authorities', sa.Column('not_before', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('authorities', sa.Column('cn', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    op.add_column('authorities', sa.Column('bits', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('authorities', sa.Column('not_after', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.alter_column('authorities', 'owner',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    ### end Alembic commands ###
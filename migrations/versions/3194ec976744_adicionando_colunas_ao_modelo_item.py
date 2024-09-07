"""Adicionando colunas ao modelo Item

Revision ID: 3194ec976744
Revises: 
Create Date: 2024-09-06 22:29:05.994049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3194ec976744'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categoria', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('tipo_venda', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('top_30', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('responsavel', sa.String(length=100), nullable=True))

    # Atualizar todas as linhas existentes com valores padrão
    op.execute("UPDATE item SET categoria = 'Não Especificado', tipo_venda = 'Normal', top_30 = 0, responsavel = 'Desconhecido'")

    # Tornar as colunas NOT NULL
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.alter_column('categoria', existing_type=sa.String(length=50), nullable=False)
        batch_op.alter_column('tipo_venda', existing_type=sa.String(length=50), nullable=False)
        batch_op.alter_column('top_30', existing_type=sa.Boolean(), nullable=False)
        batch_op.alter_column('responsavel', existing_type=sa.String(length=100), nullable=False)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_column('responsavel')
        batch_op.drop_column('top_30')
        batch_op.drop_column('tipo_venda')
        batch_op.drop_column('categoria')

    # ### end Alembic commands ###

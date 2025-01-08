"""Initial migration.

Revision ID: b71afcd74785
Revises: 
Create Date: 2025-01-08 08:58:01.983519

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b71afcd74785'
down_revision = None
branch_labels = None
depends_on = None


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('DROP TABLE IF EXISTS moyennes')
    op.execute('DROP TABLE IF EXISTS series')
    op.execute('DROP TABLE IF EXISTS universities')
    op.execute('DROP TABLE IF EXISTS posts')
    op.execute('DROP TABLE IF EXISTS matieres')
    op.execute('DROP TABLE IF EXISTS coefficients')
    op.execute('DROP TABLE IF EXISTS notes')
    op.execute('DROP TABLE IF EXISTS users')
    op.execute('DROP TABLE IF EXISTS filieres')
    op.execute('DROP TABLE IF EXISTS matiere_filiere')
    op.execute('DROP TABLE IF EXISTS ecoles')

    # ### end Alembic commands ###


def upgrade():
    op.create_table('universities',
    sa.Column('id_universite', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('nom', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('code', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id_universite', name='universities_pkey'),
    postgresql_ignore_search_path=False
    )
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ecoles',
    sa.Column('id_ecole', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('nom', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('id_universite', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('code', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_universite'], ['universities.id_universite'], name='ecoles_id_universite_fkey'),
    sa.PrimaryKeyConstraint('id_ecole', name='ecoles_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('filieres',
    sa.Column('id_filiere', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('nom', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('debouches', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('bourses', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('semi_bourses', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('code', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('id_ecole', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_ecole'], ['ecoles.id_ecole'], name='filieres_id_ecole_fkey'),
    sa.PrimaryKeyConstraint('id_filiere', name='filieres_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('matieres',
    sa.Column('id_matiere', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('nom', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id_matiere', name='matieres_pkey')
    )
    op.create_table('matiere_filiere',
    sa.Column('id_filiere', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('id_matiere', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id_filiere'], ['filieres.id_filiere'], name='matiere_filiere_id_filiere_fkey'),
    sa.ForeignKeyConstraint(['id_matiere'], ['matieres.id_matiere'], name='matiere_filiere_id_matiere_fkey'),
    sa.PrimaryKeyConstraint('id_filiere', 'id_matiere', name='matiere_filiere_pkey')
    )
    op.create_table('series',
    sa.Column('id_serie', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('nom', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id_serie', name='series_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('users',
    sa.Column('id_user', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('matricule', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('prenom', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('nom', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('role', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('id_serie', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id_serie'], ['series.id_serie'], name='users_id_serie_fkey'),
    sa.PrimaryKeyConstraint('id_user', name='users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('notes',
    sa.Column('id_user', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('id_matiere', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('mark', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id_matiere'], ['matieres.id_matiere'], name='notes_id_matiere_fkey'),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], name='notes_id_user_fkey'),
    sa.PrimaryKeyConstraint('id_user', 'id_matiere', name='notes_pkey')
    )
    op.create_table('coefficients',
    sa.Column('id_serie', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('id_matiere', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('coe', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id_matiere'], ['matieres.id_matiere'], name='coefficients_id_matiere_fkey'),
    sa.ForeignKeyConstraint(['id_serie'], ['series.id_serie'], name='coefficients_id_serie_fkey'),
    sa.PrimaryKeyConstraint('id_serie', 'id_matiere', name='coefficients_pkey')
    )
    op.create_table('posts',
    sa.Column('id_post', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('titre', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('contenu', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('adresse', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('imagePath', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id_user'], name='posts_user_id_fkey'),
    sa.PrimaryKeyConstraint('id_post', name='posts_pkey')
    )
    op.create_table('moyennes',
    sa.Column('id_filiere', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('id_user', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('average', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_filiere'], ['filieres.id_filiere'], name='moyennes_id_filiere_fkey'),
    sa.ForeignKeyConstraint(['id_user'], ['users.id_user'], name='moyennes_id_user_fkey'),
    sa.PrimaryKeyConstraint('id_filiere', 'id_user', name='moyennes_pkey')
    )
    # ### end Alembic commands ###

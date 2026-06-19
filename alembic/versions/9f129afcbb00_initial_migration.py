"""initial_migration

Revision ID: 9f129afcbb00
Revises: 
Create Date: 2026-06-19 18:47:16.353038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = '9f129afcbb00'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    op.create_table('document_chunk',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('embedding', Vector(dim=1024), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_document_chunk_embedding', 'document_chunk', ['embedding'], unique=False, postgresql_using='hnsw', postgresql_with={'m': 16, 'ef_construction': 64}, postgresql_ops={'embedding': 'vector_cosine_ops'})


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_document_chunk_embedding', table_name='document_chunk', postgresql_using='hnsw', postgresql_with={'m': 16, 'ef_construction': 64}, postgresql_ops={'embedding': 'vector_cosine_ops'})
    op.drop_table('document_chunk')
    op.execute("DROP EXTENSION IF EXISTS vector;")

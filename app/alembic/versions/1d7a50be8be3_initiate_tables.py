"""initiate tables

Revision ID: 1d7a50be8be3
Revises: 
Create Date: 2024-08-02 19:24:56.784305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d7a50be8be3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'stations',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100)),
        sa.Column('longitude', sa.Float, nullable=False),
        sa.Column('latitude', sa.Float, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False,
                  server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False,
                  server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_table(
        'metrics',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('temperature', sa.Float, nullable=False),
        sa.Column('humidity', sa.Float, nullable=False),
        sa.Column('wind_speed', sa.Float, nullable=False),
        sa.Column('wind_direction', sa.String(100), nullable=False),
        sa.Column('precipitation', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False,
                  server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, nullable=False,
                  server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column('station_id', sa.Integer,
                  sa.ForeignKey('stations.id'), nullable=False)
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('hashed_password', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False)
    )


def downgrade() -> None:
    pass

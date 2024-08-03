"""initiate tables

Revision ID: 1d7a50be8be3
Revises: 
Create Date: 2024-08-02 19:24:56.784305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import Connection
from passlib.context import CryptContext

import warnings

# Suppress specific warning from passlib
warnings.filterwarnings(
    "ignore",
    category=Warning,
    message="error reading bcrypt version"
)

# revision identifiers, used by Alembic.
revision: str = '1d7a50be8be3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


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

    # Add fixture data
    conn: Connection = op.get_bind()

    conn.execute(
        sa.text("""
            INSERT INTO stations (name, longitude, latitude, is_active, created_at, updated_at)
            VALUES 
            ('Station 1', 165.123, 83.7132, TRUE, now(), now()),
            ('Station 2', 99.0, 68.12312, TRUE, now(), now())
        """)
    )

    hashed_password = get_password_hash('testpassword')
    op.execute(
        sa.text(
            "INSERT INTO users (email, hashed_password, is_active) VALUES "
            "(:email, :hashed_password, :is_active)"
        ).bindparams(
            email='testuser@example.com',
            hashed_password=hashed_password,
            is_active=True
        )
    )

    conn.execute(
        sa.text("""
            INSERT INTO metrics (temperature, humidity, wind_speed, wind_direction, precipitation, created_at, updated_at, station_id)
            VALUES 
            (25.0, 60.0, 5.0, 'N', 0.0, now(), now(), 1),
            (20.0, 55.0, 10.0, 'E', 1.0, now(), now(), 2)
        """)
    )


def downgrade() -> None:
    op.drop_table('metrics')
    op.drop_table('stations')
    op.drop_table('users')

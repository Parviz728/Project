"""fill table users with data

Revision ID: 924b9eda2592
Revises: be947f29ec3a
Create Date: 2023-09-14 23:27:35.708763

"""
from typing import Sequence, Union
from app.auth import Auth

from alembic import op
import sqlalchemy as sa

auth = Auth()
# revision identifiers, used by Alembic.
revision: str = '924b9eda2592'
down_revision: Union[str, None] = 'be947f29ec3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user = sa.table('users',
                    sa.column('id', sa.Integer),
                    sa.column('username', sa.String),
                    sa.column('password', sa.String)
                    )

    from sqlalchemy.sql import insert
    from sqlalchemy import orm

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    data1 = {
        "username": "user1",
        "password": auth.get_password_hash("user_pass_1")
    }

    data2 = {
        "username": "user2",
        "password": auth.get_password_hash("user_pass_2")
    }

    data3 = {
        "username": "user3",
        "password": auth.get_password_hash("user_pass_3")
    }

    data4 = {
        "username": "user4",
        "password": auth.get_password_hash("user_pass_4")
    }

    data5 = {
        "username": "user5",
        "password": auth.get_password_hash("user_pass_5")
    }
    ret1 = session.execute(insert(user).values(data1))
    ret2 = session.execute(insert(user).values(data2))
    ret3 = session.execute(insert(user).values(data3))
    ret4 = session.execute(insert(user).values(data4))
    ret5 = session.execute(insert(user).values(data5))


def downgrade() -> None:
    op.execute("TRUNCATE users")

"""fill table items with data

Revision ID: be947f29ec3a
Revises: f98aee985902
Create Date: 2023-09-14 23:19:55.364077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be947f29ec3a'
down_revision: Union[str, None] = 'f98aee985902'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    item = sa.table('items',
                    sa.column('id', sa.Integer),
                    sa.column('date', sa.DATE),
                    sa.column('is_active', sa.Boolean),
                    sa.column('is_deleted', sa.Boolean)
                    )

    # If insert is required
    from sqlalchemy.sql import insert
    from sqlalchemy import orm
    import datetime

    bind = op.get_bind()
    session = orm.Session(bind=bind)

    data1 = {
        "date": datetime.datetime(2023, 1, 15),
        "is_active": False,
        "is_deleted": False
    }

    data2 = {
        "date": datetime.datetime(2023, 3, 23),
        "is_active": False,
        "is_deleted": True
    }

    data3 = {
        "date": datetime.datetime(2023, 4, 11),
        "is_active": True,
        "is_deleted": False
    }

    data4 = {
        "date": datetime.datetime(2023, 6, 10),
        "is_active": True,
        "is_deleted": True
    }

    ret1 = session.execute(insert(item).values(data1))
    ret2 = session.execute(insert(item).values(data2))
    ret3 = session.execute(insert(item).values(data3))
    ret4 = session.execute(insert(item).values(data4))


def downgrade() -> None:
    pass

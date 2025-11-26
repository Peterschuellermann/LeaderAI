"""convert_employee_notes_to_json

Revision ID: be1122f3f5e1
Revises: f1a2b3c4d5e6
Create Date: 2025-11-26 23:03:27.547120

"""
from typing import Sequence, Union
import json

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be1122f3f5e1'
down_revision: Union[str, None] = 'f1a2b3c4d5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add temporary column
    with op.batch_alter_table('employees') as batch_op:
        batch_op.add_column(sa.Column('notes_temp', sa.JSON(), nullable=True))
    
    # 2. Migrate data
    bind = op.get_bind()
    result = bind.execute(sa.text("SELECT id, notes FROM employees"))
    
    for row in result:
        emp_id = row[0]
        notes_text = row[1]
        
        notes_list = []
        if notes_text:
            notes_list.append(notes_text)
        
        # Serialize to JSON string for SQLite
        json_val = json.dumps(notes_list)
        
        bind.execute(
            sa.text("UPDATE employees SET notes_temp = :val WHERE id = :id"),
            {"val": json_val, "id": emp_id}
        )

    # 3. Drop old column and Rename new one
    with op.batch_alter_table('employees') as batch_op:
        batch_op.drop_column('notes')
        batch_op.alter_column('notes_temp', new_column_name='notes', existing_type=sa.JSON())


def downgrade() -> None:
    # 1. Add temporary column
    with op.batch_alter_table('employees') as batch_op:
        batch_op.add_column(sa.Column('notes_old', sa.Text(), nullable=True))
    
    # 2. Migrate data back
    bind = op.get_bind()
    result = bind.execute(sa.text("SELECT id, notes FROM employees"))
    
    for row in result:
        emp_id = row[0]
        notes_json = row[1]
        
        note_text = ""
        if notes_json:
             try:
                 if isinstance(notes_json, str):
                     data = json.loads(notes_json)
                 else:
                     # If SQLAlchemy returns python object (list)
                     data = notes_json
                 
                 if isinstance(data, list) and len(data) > 0:
                     note_text = "\n\n".join(str(x) for x in data)
                 elif data:
                     note_text = str(data)
             except Exception:
                 note_text = str(notes_json)

        bind.execute(
            sa.text("UPDATE employees SET notes_old = :val WHERE id = :id"),
            {"val": note_text, "id": emp_id}
        )

    # 3. Drop old column and Rename new one
    with op.batch_alter_table('employees') as batch_op:
        batch_op.drop_column('notes')
        batch_op.alter_column('notes_old', new_column_name='notes', existing_type=sa.Text())

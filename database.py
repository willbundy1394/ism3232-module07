# database.py
# Author: Will Bundy
import sqlite3


def query_all(db_file, sql, values=()):
    """Run a SELECT and return every row as a dictionary."""
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(sql, values).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def query_one(db_file, sql, values=()):
    """Run a SELECT and return the first row as a dictionary, or None."""
    rows = query_all(db_file, sql, values)
    if rows == []:
        return None
    return rows[0]


def change(db_file, sql, values=()):
    """Run an INSERT or UPDATE, save it, and return the ID of the last row inserted."""
    conn = sqlite3.connect(db_file)
    cursor = conn.execute(sql, values)
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def create_tables(db_file):
    """Create the tables and the sample rows, unless they are already there."""
    with open("schema.sql") as f:
        script = f.read()
    conn = sqlite3.connect(db_file)
    conn.executescript(script)
    conn.commit()
    conn.close()


def find_proposal(db_file, proposal_id):
    """Return one proposal, or None if there is no proposal with exactly this ID."""
    return query_one(
        db_file, "SELECT * FROM proposals WHERE proposal_id = ?", (proposal_id,)
    )


def find_equipment(db_file, item_name):
    """Return one equipment item, or None if not found."""
    return query_one(
        db_file, "SELECT * FROM equipment WHERE item_name = ?", (item_name,)
    )


def equipment_names(db_file):
    """Return a list of all equipment item names (lowercase)."""
    rows = query_all(db_file, "SELECT item_name FROM equipment")
    return [row["item_name"].lower() for row in rows]


def add_change_request(db_file, proposal_id, new_value):
    """File a new change request and return its number."""
    return change(
        db_file,
        "INSERT INTO change_requests (proposal_id, new_value) VALUES (?, ?)",
        (proposal_id, new_value),
    )


def find_request(db_file, number):
    """Return one change request by number, or None."""
    return query_one(
        db_file, "SELECT * FROM change_requests WHERE number = ?", (number,)
    )


def waiting_requests(db_file):
    """Return all change requests that are still waiting."""
    return query_all(
        db_file,
        "SELECT * FROM change_requests WHERE status = 'waiting' ORDER BY number",
    )


def approve_request(db_file, number):
    """Approve a waiting request: update the proposal's install_date, then mark approved."""
    request = find_request(db_file, number)
    if request is None:
        return f"There is no request {number}."
    if request["status"] != "waiting":
        return f"Request {number} is already {request['status']}."

    proposal_id = request["proposal_id"]
    new_value = request["new_value"]

    change(
        db_file,
        "UPDATE proposals SET install_date = ? WHERE proposal_id = ?",
        (new_value, proposal_id),
    )
    change(
        db_file,
        "UPDATE change_requests SET status = 'approved' WHERE number = ?",
        (number,),
    )
    return f"Request {number} approved."


def reject_request(db_file, number):
    """Reject a waiting request (does not change the proposal)."""
    request = find_request(db_file, number)
    if request is None:
        return f"There is no request {number}."
    if request["status"] != "waiting":
        return f"Request {number} is already {request['status']}."

    change(
        db_file,
        "UPDATE change_requests SET status = 'rejected' WHERE number = ?",
        (number,),
    )
    return f"Request {number} rejected."


def all_proposals(db_file):
    """Return every proposal (for the staff review list at the end of main.py)."""
    return query_all(db_file, "SELECT * FROM proposals ORDER BY proposal_id")

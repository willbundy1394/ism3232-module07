import database
from tools import SimplyRenewableTools


def make_tools(tmp_path):
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return SimplyRenewableTools(db_file)


def customer(text):
    return [{"role": "user", "content": text}]


def test_lookup_proposal_finds_id(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run(
        "lookup_proposal",
        {"proposal_id": "SR203"},
        customer("What is the status of SR203?"),
    )
    assert "SR203" in reply
    assert "scheduled" in reply


def test_lookup_equipment_works(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run(
        "lookup_equipment",
        {"item_name": "Critter Guard Mesh Kit"},
        customer("Do you have the Critter Guard Mesh Kit?"),
    )
    assert "15" in reply


def test_request_change_waits(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run(
        "request_change",
        {"proposal_id": "SR201", "new_value": "2026-12-19"},
        customer("Please move SR201 to 2026-12-19"),
    )
    assert "Request 1 was sent to staff" in reply
    assert len(database.waiting_requests(tools.db_file)) == 1


def test_unknown_tool_refused(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run("delete_all", {}, customer("hi"))
    assert "There is no tool named" in reply


def test_made_up_id_refused(tmp_path):
    tools = make_tools(tmp_path)
    reply = tools.run(
        "lookup_proposal",
        {"proposal_id": "SR999"},
        customer("Where is SR201?"),
    )
    assert "has not given that proposal ID" in reply

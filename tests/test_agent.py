import database
from agent import SupportChatbot
from fake_model import FakeModel
from tools import SimplyRenewableTools


def make_bot(tmp_path, model):
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return SupportChatbot("Sunny", "Be helpful.", SimplyRenewableTools(db_file), model)


def ask_for_tool(name, arguments):
    return {"tool": name, "arguments": arguments}


def test_lookup_answers_from_database(tmp_path):
    model = FakeModel(
        [
            ask_for_tool("lookup_proposal", {"proposal_id": "SR203"}),
            {"text": "Your proposal is scheduled."},
        ]
    )
    bot = make_bot(tmp_path, model)
    bot.respond("What is the status of SR203?")
    assert "SR203" in bot.history[1]["content"]


def test_made_up_change_never_reaches_database(tmp_path):
    model = FakeModel(
        [
            ask_for_tool(
                "request_change",
                {"proposal_id": "SR202", "new_value": "2026-12-25"},
            ),
            {"text": "What is the new date?"},
        ]
    )
    bot = make_bot(tmp_path, model)
    bot.respond("Please change the date on SR201")
    assert database.waiting_requests(bot.tools.db_file) == []

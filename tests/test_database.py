import database


def make_db(tmp_path):
    db_file = tmp_path / "test.db"
    database.create_tables(db_file)
    return db_file


def test_create_tables_twice_adds_no_duplicate_rows(tmp_path):
    db_file = make_db(tmp_path)
    database.create_tables(db_file)
    assert len(database.query_all(db_file, "SELECT * FROM proposals")) == 6
    assert len(database.query_all(db_file, "SELECT * FROM equipment")) == 6


def test_find_proposal_needs_the_exact_id(tmp_path):
    db_file = make_db(tmp_path)
    assert database.find_proposal(db_file, "SR203") is not None
    assert database.find_proposal(db_file, "SR999") is None


def test_sql_in_a_proposal_id_is_just_text(tmp_path):
    db_file = make_db(tmp_path)
    assert database.find_proposal(db_file, "SR201' OR '1'='1") is None


def test_change_requests_get_numbers_and_wait(tmp_path):
    db_file = make_db(tmp_path)
    number = database.add_change_request(db_file, "SR201", "2026-12-19")
    assert number == 1
    request = database.find_request(db_file, 1)
    assert request["status"] == "waiting"
    assert len(database.waiting_requests(db_file)) == 1


def test_approve_changes_the_install_date_once(tmp_path):
    db_file = make_db(tmp_path)
    database.add_change_request(db_file, "SR201", "2026-12-19")
    assert database.approve_request(db_file, 1) == "Request 1 approved."
    proposal = database.find_proposal(db_file, "SR201")
    assert proposal["install_date"] == "2026-12-19"
    assert database.approve_request(db_file, 1) == "Request 1 is already approved."
    assert database.waiting_requests(db_file) == []


def test_reject_changes_nothing(tmp_path):
    db_file = make_db(tmp_path)
    database.add_change_request(db_file, "SR202", "2026-12-25")
    assert database.reject_request(db_file, 1) == "Request 1 rejected."
    proposal = database.find_proposal(db_file, "SR202")
    assert proposal["install_date"] == "2026-12-14"

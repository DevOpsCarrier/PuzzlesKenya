import sqlite3 as lite
import pytest
from puzzleske.db import get_db



def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(lite.ProgrammingError) as e:
        db.execute('SELECT 1')
    
    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('puzzleske.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Database Initialised' in result.output
    assert Recorder.called
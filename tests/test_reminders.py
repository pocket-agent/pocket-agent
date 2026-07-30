from pathlib import Path

from pocket_agent.automation.reminders import ReminderStore


def test_reminder_add_and_list(tmp_path: Path):
    store = ReminderStore(tmp_path / "reminders.json")
    row = store.add(
        "Test message",
        "2099-01-01T12:00:00+00:00",
        user_key="local-dev",
        chat_id=None,
    )
    pending = store.list_pending(user_key="local-dev")
    assert len(pending) == 1
    assert pending[0]["id"] == row["id"]

    ok = store.cancel(row["id"], user_key="local-dev")
    assert ok
    assert store.list_pending(user_key="local-dev") == []

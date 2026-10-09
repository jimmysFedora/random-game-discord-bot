import asyncio

import pytest

from random_game_bot.bot import chunk_lines, connect, create_bot


class FakeInteraction:
    """Records messages a command sends instead of talking to Discord."""

    def __init__(self):
        self.sent = []
        self.response = self
        self.followup = self

    async def send_message(self, msg):
        self.sent.append(msg)

    async def send(self, msg):
        self.sent.append(msg)


@pytest.fixture
def db(tmp_path):
    (tmp_path / "games.csv").write_text("Portal 2\nPEAK\n\nLeft 4 Dead 2\n")
    return connect(tmp_path / "games.db")


@pytest.fixture
def bot(db):
    return create_bot(db)


def run(bot, name, **kwargs):
    interaction = FakeInteraction()
    asyncio.run(bot.tree.get_command(name).callback(interaction, **kwargs))
    return interaction.sent


def test_imports_seed_csv_once(db, tmp_path):
    assert db.execute("SELECT count(*) FROM games").fetchone()[0] == 3
    db.execute("DELETE FROM games WHERE name = 'PEAK'")
    db.commit()
    db.close()
    assert connect(tmp_path / "games.db").execute("SELECT count(*) FROM games").fetchone()[0] == 2


def test_list_sorted(bot):
    assert run(bot, "list") == ["- Left 4 Dead 2\n- PEAK\n- Portal 2"]


def test_empty_list(tmp_path):
    bot = create_bot(connect(tmp_path / "games.db"))
    assert run(bot, "list") == ["The game list is empty."]
    assert run(bot, "roll") == ["The game list is empty."]


def test_roll(bot):
    (msg,) = run(bot, "roll")
    assert msg in {"**Portal 2**", "**PEAK**", "**Left 4 Dead 2**"}


def test_add_strips_and_rejects_duplicates(bot):
    assert run(bot, "add", game="  Hades  ") == ["Added **Hades**."]
    assert run(bot, "add", game="hades") == ["**hades** is already in the list."]


def test_rm_case_insensitive_returns_stored_name(bot):
    assert run(bot, "rm", game="portal 2") == ["Removed **Portal 2**."]
    assert run(bot, "rm", game="Portal 2") == ["**Portal 2** is not in the list."]


def test_rm_autocomplete(bot):
    callback = bot.tree.get_command("rm")._params["game"].autocomplete
    choices = asyncio.run(callback(FakeInteraction(), "p"))
    assert [c.value for c in choices] == ["PEAK", "Portal 2"]


def test_command_limits_sent_to_discord(bot):
    (add_opt,) = bot.tree.get_command("add").to_dict(bot.tree)["options"]
    (rm_opt,) = bot.tree.get_command("rm").to_dict(bot.tree)["options"]
    assert add_opt["max_length"] == 100
    assert rm_opt["autocomplete"] is True


def test_long_list_split_across_messages(bot, db):
    db.executemany("INSERT INTO games (name) VALUES (?)", [(f"Game {n:03d}",) for n in range(300)])
    messages = run(bot, "list")
    assert len(messages) > 1
    assert all(len(m) <= 2000 for m in messages)
    assert sum(m.count("\n") + 1 for m in messages) == 303


def test_chunk_lines_single_line():
    assert chunk_lines(["- a"]) == ["- a"]

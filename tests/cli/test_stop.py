"""Test stop cli."""
from click.testing import CliRunner
from diligent import cli


def test_stop():
    """Test stop cli."""
    runner = CliRunner()

    result = runner.invoke(cli, ["stop"])

    assert result.exit_code == 0

"""Test start cli."""
import pytest
from click.testing import CliRunner
from diligent import cli


@pytest.mark.parametrize("filepath", ["tests/data/config.toml"])
def test_start(filepath):
    """Test start cli."""
    runner = CliRunner()

    result = runner.invoke(cli, ["start", "-t", filepath])

    assert result.exit_code == 0

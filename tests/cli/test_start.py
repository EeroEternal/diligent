"""Test start cli."""
import pytest
from click.testing import CliRunner
from diligent import cli
from diligent.cli import start_server


@pytest.mark.parametrize("filepath", ["../data/config.toml"])
def test_start(filepath):
    """Test start cli."""
    runner = CliRunner()

    result = runner.invoke(cli, ["-t", filepath, "start"])

    assert result.exit_code == 0


# @pytest.mark.parametrize("filepath", ["../data/config.toml"])
# def test_start_func(filepath):
#     """Test start function"""
#     start_server(filepath)




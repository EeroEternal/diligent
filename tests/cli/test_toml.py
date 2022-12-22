"""Test toml read."""

import pytest
from diligent.cli import obs


@pytest.mark.parametrize("filepath", ["tests/data/config.toml"])
def test_read_toml(filepath):
    """Test read toml."""
    access_key_id, secret_access_key, endpoint= obs.read_toml(filepath)

    assert access_key_id == "12345"
    assert secret_access_key == "67890"
    assert endpoint == "https://obs.cn-north-1.myhwclouds.com"

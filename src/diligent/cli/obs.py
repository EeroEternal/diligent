"""Read config file."""
import tomllib


def server_config(filepath):
    """Read server config from toml file.

    Args:
        filepath (str): toml config file path.
    Returns:
        (str, int): host, port.
    """
    with open(filepath, "rb") as f:
        config = tomllib.load(f)

        host = config["server"]["host"]
        port = config["server"]["port"]
        return host, port

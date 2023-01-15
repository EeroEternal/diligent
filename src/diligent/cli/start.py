"""Start server."""
import tomllib

from wareroom import Credential, Bucket
from ..server import Server


def server_config(toml):
    """Read server config."""
    with open(toml, 'rb') as file:
        config = tomllib.load(file)
        return config["server"]["host"], config["server"]["port"]


def start_server(toml):
    """Start the Diligent server."""
    credential = Credential.from_file(toml)

    # start server
    server = Server()

    # read bucket name from config file
    server.bucket = Bucket.from_file(toml)

    # init obs
    server.init_storage(credential)

    # set router . must behind init_obs
    server.set_router()

    # run server
    host, port = server_config(toml)
    server.run(host, port)

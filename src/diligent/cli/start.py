"""Start server."""
from wareroom import read_config

from ..server import Server
from .obs import server_config


def start_server(toml):
    """Start the Diligent server."""
    access_key_id, secret_access_key, endpoint, bucket = read_config(toml)

    # start server
    server = Server()

    # init obs
    server.init_obs(access_key_id, secret_access_key, endpoint, bucket)

    # set router . must behind init_obs
    server.set_router()

    # run server
    host, port = server_config(toml)
    server.run(host, port)

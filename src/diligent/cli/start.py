"""Start server."""

from ..auth import Credential
from ..server import Server


def server_config(toml):
    """Read server config."""
    with open(toml, 'r', encoding='utf-8') as file:
        config = toml.load(file)
        return config["server"]["host"], config["server"]["port"]


def start_server(toml):
    """Start the Diligent server."""
    credential = Credential(toml)


    # start server
    server = Server()

    # init obs
    server.init_storage(
        credential.access_key_id, credential.secret_access_key,
                    credential.endpoint, credential.bucket)

    # set router . must behind init_obs
    server.set_router()

    # run server
    host, port = server_config(toml)
    server.run(host, port)

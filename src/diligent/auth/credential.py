"""Credential management for the Diligent API."""

import tomllib


class Credential:
    """Credential class.

    :param filepath: config file path.
    :type filepath: str
    :param kind: config kind, only obs now.
    :type kind: str

    """

    def __init__(self, filepath, kind='obs'):
        """Constructor method.
        """
        result = read_config(filepath, kind)
        self.access_key_id = result["access_key_id"]
        self.secret_access_key = result["secret_access_key"]
        self.endpoint = result["endpoint"]
        self.bucket = result["bucket"]

    @property
    def access_key(self):
        """Access key property.
        """
        return self.access_key_id

    @property
    def secret_key(self):
        """Secret key property.
        """
        return self.secret_access_key

    @property
    def bucket(self):
        """Bucket name property.
        """
        return self.bucket

    @property
    def endpoint_url(self):
        """Endpoint url property.
        """
        return self.endpoint


def read_config(filepath, kind):
    """Read obs config from toml file.

    :param filepath: toml config file path.
    :type filepath: str
    :param kind: config kind, only obs now.
    :type kind: str

    :returns: dict include access_id, secret_key, endpoint, bucket.
    """
    print(f'kind: {kind}')
    with open(filepath, 'r', encoding="utf-8") as file:
        config = tomllib.load(file)

        access_key_id = config["obs"]["access_key_id"]
        secret_access_key = config["obs"]["secret_access_key"]
        endpoint = config["obs"]["endpoint"]
        bucket = config["obs"]["bucket"]

        result = {
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key,
            "endpoint": endpoint,
            "bucket": bucket
        }

        return result

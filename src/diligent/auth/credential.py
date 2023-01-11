"""Credential management for the Diligent API."""

import tomllib


class Credential:
    """Credential class.

    :param access_key_id: Access key ID.
    :type access_key_id: str
    :param secret_access_key: Secret access key.
    :type secret_access_key: str
    :param endpoint: Endpoint URL.
    :type endpoint: str
    :param kind: Storage type. As "obs" "s3" "minio" "gcs" "azure"
    :type kind: str
    """

    # pylint disable=too-many-arguments
    def __init__(self, access_key_id, secret_access_key, endpoint, kind):
        """Constructor method.
        """
        self._bucket = None
        self._access_key_id = access_key_id
        self._secret_access_key = secret_access_key
        self._endpoint = endpoint
        # kind is storage type. like "obs" "s3" "minio" "gcs" "azure"
        self._kind = kind

    @classmethod
    def from_file(cls, filepath, kind='obs'):
        """Initialize credential from config file.

        :param filepath: config file path.
        :type filepath: str
        :param kind: config kind, only obs now.
        :type kind: str

        :return: Credential object.
        :rtype: Credential
        """
        result = read_config(filepath, kind)
        return \
            cls(result['access_key_id'],
                result['secret_access_key'],
                result['endpoint'],
                kind)

    @property
    def access_key(self):
        """Access key property.
        """
        return self._access_key_id

    @property
    def secret_key(self):
        """Secret key property.
        """
        return self._secret_access_key

    @property
    def bucket(self):
        """Bucket name property.
        """
        return self._bucket

    @bucket.setter
    def bucket(self, bucket):
        """Bucket name setter.
        """
        self._bucket = bucket

    @property
    def endpoint(self):
        """Endpoint url property.
        """
        return self._endpoint


def read_config(filepath, kind):
    """Read obs config from toml file.

    :param filepath: toml config file path.
    :type filepath: str
    :param kind: config kind, only obs now.
    :type kind: str

    :returns: dict include access_id, secret_key, endpoint, bucket.
    """
    print(f'kind: {kind}')
    with open(filepath, 'rb') as file:
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

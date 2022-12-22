"""FastApi server."""

from fastapi import FastAPI, UploadFile
from fastapi.responses import Response
import uvicorn

from ..storage import Client


class Server:
    """API server."""

    def __init__(self):
        """Initialize the FastApi server."""
        self.app = FastAPI()
        self.client = None
        self.bucket = None

    def init_obs(self, access_key, secret_key, endpoint, bucket):
        """Initialize OBS backend.

        Args:
            access_key(str): OBS access key.
            secret_key (str): OBS secret access key.
            endpoint (str): OBS server address. e.g. https://obs.cn-north-1.myhwclouds.com
        """
        self.client = Client(access_key, secret_key, endpoint)
        self.bucket = bucket

    def set_router(self):
        """Initialize the FastApi server."""
        self.app = FastAPI()

        @self.app.get("/image")
        async def image(id):
            """Get image.

            Args:
                id (str): image id.

            returns:
                Response : image response.
            """
            return Response(b"image binary data", media_type="image/png")

        @self.app.get("/markdown")
        async def markdown(id):
            """Get markdown.

            Args:
                id (str): markdown id.

            returns:
                Response : markdown response.
            """
            return Response(b"markdown binary data", media_type="text/markdown")

        @self.app.post("/upload")
        async def upload(file):
            """Upload file.

            Args:
                file (UploadFile): file to upload.
            """
            filename = file.filename
            content_type = file.content_type
            result = self.client.add(self.bucket, filename, content_type, file.file)

            return {"result": result}

    def run(self, host, port):
        """Run the server.

        Args:
            host (str): server host.
            port (int): server port.
        """
        uvicorn.run(self.app, host=host, port=port)




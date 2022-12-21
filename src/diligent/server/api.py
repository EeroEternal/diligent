"""FastApi server."""

from fastapi import FastAPI, UploadFile
from fastapi.responses import Response
from ..storage import Client


class Server:
    """FastApi server."""

    def __init__(self):
        """Initialize the FastApi server."""
        self.app = FastAPI()

    def run(self):
        """Run the FastApi server."""

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
            access_id = "access_id"
            secret_key = "secret_key"
            endpoint = "https://obs.cn-north-1.myhwclouds.com"
            client = Client(access_id, secret_key, endpoint)

            bucket = "bucket"
            filename = file.filename
            content_type = file.content_type
            result = client.add(bucket, filename, content_type, file.file)

            return {"result": result}

    def stop(self):
        """Stop the FastApi server."""

    def __call__(self):
        """Call the FastApi server."""
        return self.app

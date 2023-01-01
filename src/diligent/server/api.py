"""FastApi server."""
from typing import List

from fastapi import FastAPI, UploadFile
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
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

        @self.app.post("/upload/")
        async def upload(files: List[UploadFile]):
            """Upload files.

            Args:
                files ( List[UploadFile] ): file to upload.
            """
            all_success = True

            for file in files:
                filename = file.filename
                content_type = file.content_type
                result = self.client.add(self.bucket, filename, content_type, file.file)
                if not result:
                    all_success = False

            return {"result": all_success}

        # **must** after all router, set cors middleware can work
        self._set_cors()

    def _set_cors(self):
        """Set CORS."""
        # set cors
        origins = [
            "*"
        ]

        # add cors middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def run(self, host, port):
        """Run the server.

        Args:
            host (str): server host.
            port (int): server port.
        """
        uvicorn.run(self.app, host=host, port=port)




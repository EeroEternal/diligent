"""FastApi server."""
from io import BytesIO
from typing import List

import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse

from wareroom import Client


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
            bucket (str): OBS bucket name.
        """
        self.client = Client(access_key, secret_key, endpoint)
        self.bucket = bucket

    def set_router(self):
        """Initialize the FastApi server."""
        self.app = FastAPI()

        @self.app.get("/image/{image_name}")
        async def image(image_name):
            """Get image.

            Args:
                image_name (str): image id.

            returns:
                Response : image response.
            """
            # get image
            result, content, buffer = self.client.get(self.bucket, image_name)

            if result:
                content_type = content

                # change bytes to stream
                stream = BytesIO(buffer)

                return StreamingResponse(stream, media_type=content_type)

            # return not found
            return Response(status_code=404)

        @self.app.get("/markdown")
        async def markdown(name):
            """Get markdown.

            Args:
                name (str): markdown name.

            returns:
                Response : markdown response.
            """
            print(f'get markdown {name}')
            return Response(b"markdown binary data", media_type="text/markdown")

        @self.app.post("/upload/")
        async def upload(files: List[UploadFile]):
            """Upload files.

            Args:
                files ( List[UploadFile] ): file to upload.
            """

            # upload files result list
            results = []

            for file in files:
                filename = file.filename
                content_type = file.content_type

                # upload file
                result, content = self.client.add(self.bucket, filename, content_type,
                                                  file.file)

                # add result to list
                results.append({result: result, content: content})

            return {"results": results}

        # **must** after all router, set cors middleware can work
        self._set_cors()

    def _set_cors(self):
        """Set CORS."""
        # set cors
        origins = ["*"]

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

"""FastApi server."""
from io import BytesIO
from typing import List, Tuple, overload

import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse

from wareroom import Client
from ..auth import Credential


class Server:
    """API server."""

    def __init__(self):
        """Initialize the FastApi server."""
        self.app = FastAPI()

        self.client = None
        self.bucket = None
        self.endpoint = None

    @overload
    def init_storage(self, credential: Credential):
        """Initialize credential and storage client.

        :param credential: Credential object.
        :type credential: Credential
        """

    @overload
    def init_storage(self, credential: Tuple) -> None:
        """Initialize credentials and storage client.

        :param credential: Credential information
        :type credential: Tuple.
            include (access_key_id, secret_access_key, endpoint, bucket)
        """

    def init_storage(self, credential):
        """Initialize credential and storage client.

        :param credential: Credential object.
        :type credential: different type. Credential or Tuple
        """
        if isinstance(credential, Credential):
            self.client = Client(credential.access_key_id,
                                 credential.secret_access_key,
                                 credential.endpoint)
            self.bucket = credential.bucket

        if isinstance(credential, Tuple):
            self.client = Client(credential[0], credential[1], credential[2])
            self.bucket = credential[3]

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

            :param name: markdown name.
            :type name: str

            :return: markdown content.
            """
            print(f'get markdown {name}')
            return Response(b"markdown binary data", media_type="text/markdown")

        @self.app.post("/upload/")
        async def upload(files: List[UploadFile]):
            """Upload files.

            :param files: files to upload.
            :type files: List[UploadFile]
            """

            # upload files result list
            results = []

            for file in files:
                filename = file.filename
                content_type = file.content_type

                # upload file
                result, content = self.client.add(self.bucket, filename,
                                                  content_type, file.file)

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

        :param host: host.
        :type host: str
        :param port: port.
        :type port: int
        """
        uvicorn.run(self.app, host=host, port=port)

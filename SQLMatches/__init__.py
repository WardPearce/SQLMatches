# -*- coding: utf-8 -*-

"""
GNU General Public License v3.0 (GPL v3)
Copyright (c) 2020-2021 WardPearce
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


import logging
import bcrypt
import backblaze
import aiobotocore

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from SQLMatchesBase import SQLMatchesBase
from typing import Dict, List, Tuple
from datetime import timedelta
from aiocache import Cache

from .resources import Sessions, Config

from .settings.upload import (
    B2UploadSettings,
    LocalUploadSettings,
    S3UploadSettings
)

from .middlewares import APIAuthentication

from .routes import ROUTES, ERROR_HANDLERS
from .routes.errors import auth_error

from .key_loader import KeyLoader

from .constants import MAP_IMAGES


__version__ = "1.0.0"
__url__ = "https://github.com/SQLMatches"
__description__ = "SQLMatches, match & demos recorder."
__author__ = "WardPearce"
__author_email__ = "wardpearce@protonmail.com"
__license__ = "GPL v3"


logger = logging.getLogger("SQLMatches")


class SQLMatches(Starlette):
    def __init__(self, base_settings: SQLMatchesBase,
                 root_steam_id: str,
                 upload_settings: Tuple[
                     B2UploadSettings,
                     S3UploadSettings,
                     LocalUploadSettings
                 ] = None,
                 map_images: Dict[str, str] = MAP_IMAGES,
                 free_upload_size: float = 30.0,
                 max_upload_size: float = 100.0,
                 match_timeout: timedelta = timedelta(hours=3),
                 demo_expires: timedelta = timedelta(weeks=20),
                 clear_cache: bool = True,
                 **kwargs) -> None:

        self.__base_settings = base_settings

        startup_tasks = [self._startup]
        shutdown_tasks = [self._shutdown]

        if "on_startup" in kwargs:
            startup_tasks = startup_tasks + kwargs["on_startup"]

        if "on_shutdown" in kwargs:
            shutdown_tasks = shutdown_tasks + kwargs["on_shutdown"]

        middlewares = [
            Middleware(
                SessionMiddleware,
                secret_key=KeyLoader(name="session").load()
            ),
            Middleware(
                AuthenticationMiddleware,
                backend=APIAuthentication(),
                on_error=auth_error
            ),
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_methods=["GET", "POST", "DELETE", "OPTIONS"]
            )
        ]

        if "middleware" in kwargs:
            middlewares = middlewares + kwargs["middleware"]

        if "routes" in kwargs:
            self.__routes = kwargs["routes"] + ROUTES
        else:
            self.__routes = ROUTES

        if "exception_handlers" in kwargs:
            exception_handlers = kwargs["exception_handlers"] + ERROR_HANDLERS
        else:
            exception_handlers = ERROR_HANDLERS

        Config.map_images = map_images
        Config.free_upload_size = free_upload_size
        Config.max_upload_size = max_upload_size
        Config.root_steam_id_hashed = bcrypt.hashpw(
            root_steam_id.encode(), bcrypt.gensalt()
        )
        Config.match_timeout = match_timeout
        Config.demo_expires = demo_expires
        Config.upload = upload_settings

        self.__clear_cache = clear_cache

        super().__init__(
            routes=self.__routes,
            exception_handlers=exception_handlers,
            middleware=middlewares,
            on_startup=startup_tasks,
            on_shutdown=shutdown_tasks,
            **kwargs
        )

    async def _startup(self) -> None:
        """Creates needed sessions.
        """

        if Config.upload_settings:
            if isinstance(Config.upload_settings, B2UploadSettings):
                Config.upload_type = B2UploadSettings

                self.b2 = backblaze.Awaiting(
                    Config.upload_settings.key_id,
                    Config.upload_settings.application_key
                )

                Sessions.bucket = self.b2.bucket(
                    Config.upload_settings.bucket_id
                )

            elif isinstance(Config.upload_settings, S3UploadSettings):
                Config.upload_type = S3UploadSettings

                Sessions.bucket = await (
                    aiobotocore.get_session()
                ).create_client(
                    "s3",
                    region_name=Config.upload_settings.region_name,
                    aws_secret_access_key=(
                        Config.upload_settings.secret_access_key
                    ),
                    aws_access_key_id=Config.upload_settings.access_key_id
                ).__aenter__()

                logger.warning("""Unlike B2, S3 requires the entire
                demo to be downloaded into memory in-order to upload it.
                For scalability B2 allows to upload demos in 5mb parts.""")

            elif isinstance(Config.upload_settings, LocalUploadSettings):
                Config.upload_type = LocalUploadSettings

                # Dynamically adding mount if local storage.

                # Name attribute for Mount isn't working correctly here,
                # so please don't change '/demos/'.
                for mount in self.__routes:
                    if type(mount) == Mount and mount.name == "api":
                        mount.app.routes.append(
                            Mount(
                                "/demos/",
                                StaticFiles(
                                    directory=Config.upload_settings.pathway
                                )
                            )
                        )
                        break

                logger.warning(
                    """Local storage isn't recommend for production use.
                    Use B2 or S3 for production."""
                )
            else:
                raise Exception("Invalid `Config.upload_settings` class.")
        else:
            Config.upload_type = None

        await self.__base_settings.startup()

        try:
            Sessions.cache = Cache(Cache.REDIS)
            await Sessions.cache.exists("connection")
        except ConnectionRefusedError:
            Sessions.cache = Cache(Cache.MEMORY)
            logger.warning(
                "Memory cache being used, use redis for production."
            )

        if self.__clear_cache:
            await Sessions.cache.clear()

        if Config.upload_type == B2UploadSettings:
            await self.b2.authorize()

    async def _shutdown(self) -> None:
        """Closes any underlying sessions.
        """

        await self.__base_settings.shutdown()
        await Sessions.cache.close()

        if Config.upload_type == B2UploadSettings:
            await self.b2.close()
        elif Config.upload_type == S3UploadSettings:
            # Not sure if this works.
            await Sessions.bucket.__aexit__(None, None, None, None)

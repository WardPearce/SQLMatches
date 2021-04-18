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


from starlette.routing import Route, Mount
from starlette.exceptions import HTTPException

from webargs_starlette import WebargsHTTPException

# Routes
from .steam import (
    SteamValidate,
    SteamLogin,
    SteamLogout
)
from .errors import (
    server_error,
    payload_error
)


ERROR_HANDLERS = {
    WebargsHTTPException: payload_error,
    HTTPException: server_error
}


ROUTES = [
    Mount("/api", name="api", routes=[
        Mount("/steam", routes=[
            Route("/login", SteamLogin),
            Route("/validate", SteamValidate),
            Route("/logout", SteamLogout)
        ]),
    ])
]

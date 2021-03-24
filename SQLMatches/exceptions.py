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


class SQLMatchesException(Exception):
    """Base Exception for SQLMatches.
    """

    def __init__(self, msg: str = "Internal error", status_code: int = 500,
                 *args, **kwargs):
        self.status_code = status_code
        super().__init__(msg, *args, **kwargs)


class CommunityTaken(SQLMatchesException):
    """Raised when community name is taken.
    """

    def __init__(self, msg: str = "Community name taken",
                 status_code: int = 400, *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class MaxCommunities(SQLMatchesException):
    """Raised when user has reached community limit.
    """

    def __init__(self, msg: str = "Community limit reached",
                 status_code: int = 400, *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class InvalidCommunity(SQLMatchesException):
    """Raised when community ID doesn't exist.
    """

    def __init__(self, msg: str = "Invalid community",
                 status_code: int = 404, *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class NoOwnership(SQLMatchesException):
    """Raised when steam id doesn't own any communties.
    """

    def __init__(self, msg="User owns no communities", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class InvalidMatchID(SQLMatchesException):
    """Raised when match ID is invalid.
    """

    def __init__(self, msg: str = "Invalid Match ID", status_code: int = 404,
                 *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class InvalidAPIKey(SQLMatchesException):
    """Raised when API key is invalid.
    """

    def __init__(self, msg: str = "Invalid API Key", status_code: int = 401,
                 *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class DemoAlreadyUploaded(SQLMatchesException):
    """Raised when a demo has already been uploaded.
    """

    def __init__(self, msg: str = "Demo already uploaded",
                 status_code: int = 400, *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class InvalidSteamID(SQLMatchesException):
    """Raised when Steam ID isn't valid
    """

    def __init__(self, msg: str = "Invalid Steam ID", status_code: int = 404,
                 *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class InvalidCommunityName(SQLMatchesException):
    """Raised when community name isn't alphanumeric
       or character length is above 32 or below 4.
    """

    def __init__(self, msg: str = "Community name invalid",
                 status_code: int = 400, *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class InvalidCommunityType(SQLMatchesException):
    """Raised when community type isn't valid.
    """

    def __init__(self, msg: str = "Commany type invalid",
                 status_code: int = 400, *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class UserExists(SQLMatchesException):
    """Raised when user exists.
    """

    def __init__(self, msg: str = "User exists", status_code: int = 400,
                 *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class InvalidWebhook(SQLMatchesException):
    """Raised when webhook URL is invalid.
    """

    def __init__(self, msg: str = "Invalid webhook url",
                 status_code: int = 400, *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class InvalidEmail(SQLMatchesException):
    """Raised when email is invalid.
    """

    def __init__(self, msg: str = "Invalid email", status_code: int = 400,
                 *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class InvalidCustomer(SQLMatchesException):
    """Raised when customer ID is invalid.
    """

    def __init__(self, msg: str = "Invalid stripe customer ID",
                 status_code: int = 404, *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class InvalidVersion(SQLMatchesException):
    """Raised when version invalid.
    """

    def __init__(self, msg: str = "Invalid version", status_code: int = 404,
                 *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class ServerExists(SQLMatchesException):
    """Raised when server already exists.
    """

    def __init__(self, msg: str = "Server exists", status_code: int = 400,
                 *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)


class InvalidServer(SQLMatchesException):
    """Raised when server doesn't exists.
    """

    def __init__(self, msg: str = "Invalid server", status_code: int = 404,
                 *args, **kwargs):
        super().__init__(msg=msg, status_code=status_code, *args, **kwargs)

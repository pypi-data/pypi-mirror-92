"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides our interface for quering the WHOIS Record of a given subject.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/dev/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import functools
import socket
from socket import SOCK_STREAM
from typing import Optional, Union

from PyFunceble.checker.syntax.domain_base import DomainSyntaxCheckerBase
from PyFunceble.dataset.iana import IanaDataset
from PyFunceble.query.record.whois import WhoisQueryToolRecord
from PyFunceble.query.whois.converter.expiration_date import ExpirationDateExtractor


class WhoisQueryTool:
    """
    Provides the interface to get the WHOIS record of a given subject.
    """

    BUFFER_SIZE: int = 4096
    STD_PORT: int = 43

    expiration_date_extractor: ExpirationDateExtractor = ExpirationDateExtractor()
    domain_syntax_checker_base: DomainSyntaxCheckerBase = DomainSyntaxCheckerBase()
    iana_dataset: IanaDataset = IanaDataset()

    record: Optional[str] = None

    _subject: Optional[str] = None
    _server: Optional[str] = None
    _query_timeout: float = 5.0

    lookup_record: Optional[WhoisQueryToolRecord] = None

    def __init__(
        self,
        subject: Optional[str] = None,
        *,
        server: Optional[str] = None,
        query_timeout: Optional[float] = None,
    ) -> None:
        if subject is not None:
            self.subject = subject

        if server is not None:
            self.server = server

        if query_timeout is not None:
            self.set_query_timeout(query_timeout)

    def ensure_subject_is_given(func):  # pylint: disable=no-self-argument
        """
        Ensures that the subject is given before running the decorated method.

        :raise TypeError:
            If the subject is not a string.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## Safety!
            if not isinstance(self.subject, str):
                raise TypeError(
                    f"<self.subject> should be {str}, {type(self.subject)} given."
                )

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def update_lookup_record(func):  # pylint: disable=no-self-argument
        """
        Ensures that a clean record is generated after the execution of
        the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            if self.lookup_record is None or self.subject != self.lookup_record.subject:
                self.lookup_record = WhoisQueryToolRecord(port=self.STD_PORT)
                self.lookup_record.subject = self.subject

            if self.query_timeout != self.lookup_record.query_timeout:
                self.lookup_record.query_timeout = self.query_timeout

            if self.record != self.lookup_record.record:
                self.lookup_record.record = self.record

            return result

        return wrapper

    def update_lookup_record_record(func):  # pylint: disable=no-self-argument
        """
        Ensures that the record of the decorated method is set as response
        in our record.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## Just common sense
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            if result != self.lookup_record.record:
                self.lookup_record.response = result

            return result

        return wrapper

    def update_lookup_record_expiration_date(
        func,
    ):  # pylint: disable=no-self-argument
        """
        Ensures that the record of the decorated method is set as response
        in our record.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## Just common sense
            result = func(self, *args, **kwargs)  # pylint: disable=not-callable

            if result != self.lookup_record.expiration_date:
                self.lookup_record.response = result

            return result

        return wrapper

    def reset_record(func):  # pylint: disable=no-self-argument
        """
        Resets the record before executing the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## Safety!
            self.record = None

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    def query_record(func):  # pylint: disable=no-self-argument
        """
        Queries the record before executin the decorated method.
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):  # pragma: no cover ## Safety!
            self.query()

            return func(self, *args, **kwargs)  # pylint: disable=not-callable

        return wrapper

    @property
    def subject(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_subject` attribute.
        """

        return self._subject

    @subject.setter
    @reset_record
    @update_lookup_record
    def subject(self, value: str) -> None:
        """
        Sets the subject to work with.

        :param value:
            The subject to set.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._subject = value

    def set_subject(self, value: str) -> "WhoisQueryTool":
        """
        Sets the subject to work with.

        :param value:
            The subject to set.
        """

        self.subject = value

        return self

    @property
    def server(self) -> Optional[str]:
        """
        Provides the current state of the :code:`_server` attribute.
        """

        return self._server

    @server.setter
    @reset_record
    @update_lookup_record
    def server(self, value: str) -> None:
        """
        Sets the server to communicate with.

        :param value:
            The server to work with.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`str`.
        :raise ValueError:
            When the given :code:`value` is empty.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}, {type(value)} given.")

        if not value:
            raise ValueError("<value> should not be empty.")

        self._server = value

    def set_server(self, value: str) -> "WhoisQueryTool":
        """
        Sets the server to communicate with.

        :param value:
            The server to work with.
        """

        self.server = value

        return self

    @property
    def query_timeout(self) -> float:
        """
        Provides the current state of the :code:`_query_timeout` attribute.
        """

        return self._query_timeout

    @query_timeout.setter
    def query_timeout(self, value: Union[float, int]) -> None:
        """
        Sets the query_timeout to apply.

        :param value:
            The query_timeout to apply.

        :raise TypeError:
            When the given :code:`value` is not a :py:class:`int`
            nor :py:class:`float`.
        :raise ValueError:
            When the given :code:`value` is less than `1`.
        """

        if not isinstance(value, (int, float)):
            raise TypeError(f"<value> should be {int} or {float}, {type(value)} given.")

        if value < 1:
            raise ValueError(f"<value> ({value!r}) should be less than 1.")

        self._query_timeout = float(value)

    def set_query_timeout(self, value: Union[float, int]) -> "WhoisQueryTool":
        """
        Sets the query_timeout to apply.

        :param value:
            The query_timeout to apply.
        """

        self.query_timeout = value

        return self

    @ensure_subject_is_given
    def get_whois_server(self) -> Optional[str]:
        """
        Provides the whois server to work with.
        """

        extension = self.domain_syntax_checker_base.set_subject(
            self.subject
        ).get_extension()

        if self.iana_dataset.is_extension(extension):
            return self.iana_dataset.get_whois_server(extension)

        return None

    def get_lookup_record(
        self,
    ) -> Optional[WhoisQueryToolRecord]:  # pragma: no cover ## It's just a dataclass
        """
        Provides the current query record.
        """

        return self.lookup_record

    @ensure_subject_is_given
    @update_lookup_record
    def query(self) -> "WhoisQueryTool":
        """
        Queries the WHOIS record and return the current object.
        """

        if not self.server:
            whois_server = self.get_whois_server()
        else:
            whois_server = self.server

        self.lookup_record.server = whois_server
        self.lookup_record.query_timeout = self.query_timeout

        if whois_server and not self.record:
            req = socket.socket(socket.AF_INET, SOCK_STREAM)
            req.settimeout(self.query_timeout)

            try:
                req.connect((whois_server, self.STD_PORT))
                could_connect = True
            except socket.error:
                could_connect = False

            if could_connect:
                req.send(f"{self.subject}\r\n".encode())

                response = "".encode()

                while True:
                    try:
                        data = req.recv(self.BUFFER_SIZE)
                    except (ConnectionResetError, socket.timeout):
                        req.close()
                        break

                    response += data

                    if not data:
                        req.close()
                        break

                try:
                    self.record = response.decode()
                except UnicodeDecodeError:
                    # Note: Because we don't want to deal with other issue, we
                    # decided to use `replace` in order to automatically replace
                    # all non utf-8 encoded characters.
                    self.record = response.decode("utf-8", "replace")

        return self

    @query_record
    @update_lookup_record_record
    def get_record(self) -> Optional[str]:
        """
        Provides the current record.
        """

        return self.record

    @query_record
    @update_lookup_record_expiration_date
    def get_expiration_date(self) -> Optional[str]:
        """
        Provides the expiration date of the record.
        """

        if self.record:
            return self.expiration_date_extractor.set_data_to_convert(
                self.record
            ).get_converted()

        return None

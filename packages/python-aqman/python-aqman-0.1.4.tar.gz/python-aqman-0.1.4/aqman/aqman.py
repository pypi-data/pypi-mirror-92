"""Asynchronous Python client for AQMAN101 from RadonFTLabs"""
import asyncio
import socket
from typing import Any, Optional, List
import subprocess

import aiohttp
import async_timeout
from yarl import URL

from .__version__ import __version__
from .exceptions import AqmanError, AqmanConnectionError
from .models import Device, UserInfo
from .const import BASE_URL, SUPPORTED_INTERFACES
from .utils import get_ip_address, get_interfaces


class AqmanUser:
    """Main class for handling connections with an AQMAN101"""

    def __init__(
            self,
            host: str = None,
            port: int = 8297,
            request_timeout: int = 10,
            session: aiohttp.ClientSession = None):
        """Initialize the AqmanUser class"""
        self._session = session
        self._host = host
        self._port = port
        self._request_timeout = request_timeout
        self._interfaces = None
        self._host_ip = None

        # Sets the variables _interfaces, _host_ip, and _host
        self._find_host_ip()

    def _find_host_ip(self):
        interfaces = get_interfaces()
        self._interfaces = interfaces

        for interface in SUPPORTED_INTERFACES:
            if interface in interfaces:
                ip_address = get_ip_address(interface)
                self._host_ip = ip_address
                break

        self._host = f"{ip_address}:{self._port}/api"

    async def _request(self, uri: str, data: Optional[dict] = None,) -> Any:
        """Handle a request to a Aqman101"""
        url = URL.build(scheme="http", host=self._host, path=f"/{uri}")
        method = "GET"

        if self._session is None:
            self._session = aiohttp.ClientSession()

        try:
            with async_timeout.timeout(self._request_timeout):
                response = await self._session.request(
                    method, str(url)
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise AqmanConnectionError(
                "Timeout occurred while connecting to Aqman 101"
            ) from exception
        except (
            aiohttp.ClientError,
            aiohttp.ClientResponseError,
            socket.gaierror,
        ) as exception:
            raise AqmanConnectionError(
                "Error occurred while communicating with Aqman 101"
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise AqmanError(
                "Unexpected response from the Aqman 101",
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def devices_info(self) -> List[str]:
        """Get the list of serial numbers for current user of Aqman101"""
        data = await self._request("devices")
        return UserInfo.from_list(data['devices'])

    async def close(self) -> None:
        """Close open client session."""
        if self._session:
            await self._session.close()

    async def __aenter__(self) -> "Aqman":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()


class AqmanDevice:
    """Class for handling single connection with an AQMAN101"""

    def __init__(
            self,
            deviceid: str = None,
            host: str = None,
            port: int = 8297,
            request_timeout: int = 10,
            session: aiohttp.ClientSession = None) -> None:
        """Initialize Connection with AQMAN101"""
        self._deviceid = deviceid
        self._session = session
        self._host = host
        self._port = port
        self._request_timeout = request_timeout
        self._interfaces = None
        self._host_ip = None

        # Sets the variables _interfaces, _host_ip, and _host
        self._find_host_ip()

    def _find_host_ip(self):
        interfaces = get_interfaces()
        self._interfaces = interfaces

        for interface in SUPPORTED_INTERFACES:
            if interface in interfaces:
                ip_address = get_ip_address(interface)
                self._host_ip = ip_address
                break

        self._host = f"{ip_address}:{self._port}/api"

    async def _request(self, uri: str, data: str,) -> Any:
        """Handle a request to a Aqman101"""
        # Scheme is HTTP!!
        url = URL.build(scheme="http", host=self._host, path=f"/{uri}/{data}")
        method = "GET"

        if self._session is None:
            self._session = aiohttp.ClientSession()

        try:
            with async_timeout.timeout(self._request_timeout):
                response = await self._session.request(
                    method, str(url)
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise AqmanConnectionError(
                "Timeout occurred while connecting to Aqman 101"
            ) from exception
        except (
            aiohttp.ClientError,
            aiohttp.ClientResponseError,
            socket.gaierror,
        ) as exception:
            from datetime import datetime

            now = datetime.now()

            current_time = now.strftime("%Y/%m/%d, %H:%M:%S")
            error_data = {
                "sn": data,
                "dsm101_sn": "",
                "dt": current_time,
                "temp": -2,
                "humi": -2,
                "co2": -2,
                "pm1": -2,
                "pm2d5": -2,
                "pm10": -2,
                "radon": -2,
                "tvoc": -2,
            }
            return error_data
            # raise AqmanConnectionError(
            #     "Error occurred while communicating with Aqman 101"
            # ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise AqmanError(
                "Unexpected response from the Aqman 101",
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def state(self) -> Device:
        """Get the current state of Aqman101"""
        data = await self._request("device", self._deviceid)
        return Device.from_dict(data)

    async def close(self) -> None:
        """Close open client session."""
        if self._session:
            await self._session.close()

    async def __aenter__(self) -> "Aqman":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()

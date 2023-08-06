"""
Python wrapper package for the AIS API.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket
import aiohttp
import async_timeout
from .const import AIS_WS_TTS_URL, AIS_WS_COMMAND_URL, AIS_WS_AUDIO_TYPE_URL, AIS_WS_AUDIO_NAME_URL

_LOGGER = logging.getLogger(__name__)


class AisWebService(object):
    """A class for the AIS WS API."""

    def __init__(self, loop, session, api_key, ais_ws_url):
        """Initialize the class."""
        self._loop = loop
        self._session = session
        self._api_key = api_key
        self._headers = {"Authorization": api_key}
        self._ais_ws_url = ais_ws_url

    async def say_it(self, text):
        """Get tracking information."""
        url = AIS_WS_TTS_URL.format(ais_url=self._ais_ws_url, text=text)
        try:
            async with async_timeout.timeout(8, loop=self._loop):
                response = await self._session.get(url, headers=self._headers)
                result = await response.text()
                try:
                    if response.status == 200:
                        return result
                    else:
                        _LOGGER.error("Error code %s ", response.status)
                except (TypeError, KeyError) as error:
                    _LOGGER.error('Error parsing data from AIS, %s', error)
        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error connecting to AIS, %s', error)
        return ""

    async def command(self, command, value):
        """Get tracking information."""
        url = AIS_WS_COMMAND_URL.format(ais_url=self._ais_ws_url)
        requests_json = {command: value}
        try:
            async with async_timeout.timeout(8, loop=self._loop):
                response = await self._session.post(url, json=requests_json, headers=self._headers)
                result = await response.text()
                try:
                    if response.status == 200:
                        return result
                    else:
                        _LOGGER.error("Error code %s ", response.status)
                except (TypeError, KeyError) as error:
                    _LOGGER.error('Error parsing data from AIS, %s', error)
        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error connecting to AIS, %s', error)
        return ""



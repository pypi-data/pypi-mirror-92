#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Alexa devices (echo dot, etc) programmatically.

This provides a login by proxy method.

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""
import logging
from typing import Text

from aiohttp import web
from bs4 import BeautifulSoup
import multidict
from yarl import URL

from alexapy.aiohttp.client_exceptions import ClientConnectionError
from alexapy.alexalogin import AlexaLogin
from alexapy.helpers import hide_email, hide_password
from alexapy.stackoverflow import get_open_port

_LOGGER = logging.getLogger(__name__)


class AlexaProxy:
    """Class to handle proxy login connections to Alexa."""

    def __init__(self, login: AlexaLogin, base_url: Text) -> None:
        """Initialize proxy object.

        Args:
            login (AlexaLogin): AlexaLogin object to update after completion of proxy.
            base_url (Text): base url for proxy location. e.g., http://192.168.1.1

        """
        self._login: AlexaLogin = login
        self._base_url: Text = str(base_url)
        self._port: int = 0
        self.runner = None
        self.data = {}
        self._config_flow_id: Text = ""
        self._callback_url: Text = ""

    @property
    def port(self) -> int:
        """Return port."""
        return self._port

    def access_url(self) -> URL:
        """Return access url for proxy."""
        return f"{URL(self._base_url).with_port(self.port)}/"

    async def start_handler(self, request: web.Request) -> web.Response:
        """Handle start of proxy interaction.

        This will attempt a login starting at the Alexa oauth signin page.

        Args
            request (web.Request): The request to process

        Returns
            web.Response: The webresponse to display in the browser

        """
        self._config_flow_id = request.query["config_flow_id"]
        self._callback_url = request.query["callback_url"]
        await self._login.reset()
        site: URL = self._login.start_url
        _LOGGER.debug(
            "Starting auth at %s for domain %s for configflow %s with callback %s",
            site,
            self._login.url,
            self._config_flow_id,
            self._callback_url,
        )
        headers = self._change_headers(site, request)
        try:
            resp = await self._login._session.get(site, headers=headers)
        except ClientConnectionError as ex:
            return web.Response(text=f"Error connecting to {site}; please retry: {ex}")
        if self._login._debug:
            await self._login._process_resp(resp)
        text = self.change_host_to_proxy(await resp.text())
        text = self.autofill(
            text,
            {
                "email": self._login.email,
                "password": self._login.password,
                "otpCode": self._login.get_totp_token(),
            },
        )
        return web.Response(text=text, content_type=resp.content_type,)

    async def get_handler(self, request: web.Request) -> web.Response:
        """Handle get requests.

        Args
            request (web.Request): The get request to process

        Returns
            web.Response: The webresponse to the browser

        """

        _LOGGER.debug("Get Request: %s", request.url)
        if request.url.path == "/":
            return await self.start_handler(request)
        if request.url.path == "/resume" and self._login.lastreq:
            _LOGGER.debug("Resuming request: %s", self._login.lastreq)
            self._config_flow_id = request.query["config_flow_id"]
            self._callback_url = request.query["callback_url"]
            resp = self._login.lastreq
        else:
            site = URL(self.change_proxy_to_host(str(request.url)))
            headers = self._change_headers(site, request)
            try:
                resp = await self._login._session.get(site, headers=headers)
            except ClientConnectionError as ex:
                return web.Response(
                    text=f"Error connecting to {site}; please retry: {ex}"
                )
        if self._login._debug:
            await self._login._process_resp(resp)
        content_type = resp.content_type
        if content_type == "text/html":
            text = self.change_host_to_proxy(await resp.text())
            text = self.autofill(
                text,
                {
                    "email": self._login.email,
                    "password": self._login.password,
                    "otpCode": self._login.get_totp_token(),
                },
            )
            return web.Response(text=text, content_type=content_type,)
        # handle non html content
        return web.Response(body=await resp.content.read(), content_type=content_type)

    async def post_handler(self, request: web.Request) -> web.Response:
        """Handle post requests.

        Args
            request (web.Request): The post request to process

        Returns
            web.Response: The webresponse to the browser

        Raises
            web.HTTPFound: Redirect URL upon success

        """

        _LOGGER.debug("Post Request: %s", request.url)
        data = await request.post()
        self.data.update(data)
        site = URL(self.change_proxy_to_host(str(request.url)))
        headers = self._change_headers(site, request)
        try:
            # submit post
            resp = await self._login._session.post(site, data=data, headers=headers)
        except ClientConnectionError as ex:
            return web.Response(text=f"Error connecting to {site}; please retry: {ex}")
        if self._login._debug:
            await self._login._process_resp(resp)
        text = await resp.text()
        content_type = resp.content_type
        if self.data.get("email"):
            self._login.email = self.data.get("email")
        if self.data.get("password"):
            self._login.password = self.data.get("password")
        if resp.url.path in ["/ap/maplanding", "/spa/index.html"]:
            self._login.access_token = resp.url.query.get("openid.oa2.access_token")
            if self._callback_url:
                _LOGGER.debug(
                    "Proxy success for %s - %s. Redirecting to: %s",
                    self._login.email,
                    self._login.url,
                    self._callback_url,
                )
                raise web.HTTPFound(location=URL(self._callback_url))
            return web.Response(
                text=f"Successfully logged in as {self._login.email} for flow {self._config_flow_id}. Please close the window.",
            )
        text = self.change_host_to_proxy(text)
        text = self.autofill(
            text,
            {
                "email": self._login.email,
                "password": self._login.password,
                "otpCode": self._login.get_totp_token(),
            },
        )
        return web.Response(text=text, content_type=content_type)

    async def start_proxy(self) -> None:
        """Start proxy."""

        app = web.Application()
        app.add_routes(
            [
                web.route("get", "/{tail:.*}", self.get_handler),
                web.route("post", "/{tail:.*}", self.post_handler),
            ]
        )
        self.runner = web.AppRunner(app)
        await self.runner.setup()
        if not self.port:
            self._port = get_open_port()
        site = web.TCPSite(self.runner, "0.0.0.0", self.port)
        await site.start()
        _LOGGER.debug("Starting proxy at %s", f"{self._base_url}:{self.port}")

    async def stop_proxy(self):
        """Stop proxy."""
        _LOGGER.debug("Stopping proxy at %s", f"{self._base_url}:{self.port}")
        await self.runner.cleanup()
        await self.runner.shutdown()

    def change_proxy_to_host(self, text: Text) -> Text:
        """Replace text with proxy address.

        Args
            text (Text): text to replace

        Returns
            Text: Result of replacing

        """
        if self._login.oauth_login:
            return text.replace(self.access_url(), "https://www.amazon.com/")
        return text.replace(self.access_url(), f"https://www.{self._login.url}/")

    def change_host_to_proxy(self, text: Text) -> Text:
        """Replace text with Amazon address.

        Args
            text (Text): text to replace

        Returns
            Text: Result of replacing

        """
        if self._login.oauth_login:
            return text.replace("https://www.amazon.com/", self.access_url())
        return text.replace(f"https://www.{self._login.url}/", self.access_url())

    def _change_headers(self, site, request) -> dict:
        # necessary since MultiDict.update did not appear to work
        headers = multidict.MultiDict(request.headers)
        result = {}
        for k, value in headers.items():
            result[k] = value
        # _LOGGER.debug("Original headers %s", headers)
        if result.get("Host"):
            result.pop("Host")
        if result.get("Origin"):
            result["Origin"] = f"https://{site.host}"
        if result.get("Referer") and URL(result.get("Referer")).query.get(
            "config_flow_id"
        ):
            result.pop("Referer")
        elif result.get("Referer"):
            result["Referer"] = self.change_proxy_to_host(result.get("Referer"))
        # _LOGGER.debug("Final headers %s", result)
        return result

    def autofill(self, html: Text, items: dict) -> Text:
        """Autofill input tags in form in html.

        Args
            html (Text): html to convert
            items (dict): Dictionary of values to fill

        Returns
            Text: html with values filled in

        """
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        for item, value in items.items():
            for html_tag in soup.find_all(attrs={"name": item}):
                html_tag["value"] = value
                if self._login._debug:
                    _LOGGER.debug(
                        "Filled %s",
                        str(html_tag).replace(
                            value,
                            hide_password(value)
                            if item == "password"
                            else hide_email(value)
                            if item == "email"
                            else value,
                        ),
                    )
        return str(soup)

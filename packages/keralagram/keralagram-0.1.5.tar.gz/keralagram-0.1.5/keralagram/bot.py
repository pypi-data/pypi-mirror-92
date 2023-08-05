import asyncio
import json
import logging

from keralagram.errors import TelegramConnectionError
from keralagram.utils import convert_markup, HTTP
from keralagram.types import Update, Message, User
API_TIMEOUT = 60
RETRY_TIMEOUT = 30


class KeralaGram:
    def __init__(self, token: str, skip_updates: bool = False, workers: int = None, plugins: dict = None):
        self._api_url = f"https://api.telegram.org/bot{token}/"
        self._file_url = f"https://api.telegram.org/file/bot{token}/"
        self._session = HTTP
        self._loop = asyncio.get_event_loop()
        self.logger = logging.getLogger(__name__)
        self._skip_pending = skip_updates
        self._offset = 0
        self._api_timeout = API_TIMEOUT
        self._commands = []
        self.plugins = plugins

    async def send_message(
            self,
            chat_id: int,
            text: str,
            reply_message_id: int = None,
            disable_preview: bool = None,
            parse_mode: str = None,
            reply_markup=None,
            disable_notification=None
    ):
        method = r'sendMessage'
        payload = {'chat_id': str(chat_id), 'text': text}
        if reply_message_id:
            payload['reply_to_message_id'] = reply_message_id
        if disable_preview:
            payload['disable_web_page_preview'] = disable_preview
        if parse_mode:
            payload['parse_mode'] = parse_mode
        if disable_notification:
            payload['disable_notification'] = disable_notification
        if reply_markup:
            payload['reply_markup'] = convert_markup(reply_markup)

        if self._skip_pending:
            json_updates = await self._aio_post(self._get_api_url(method), payload)
            self.logger.warning(json_updates)

            return Message._de_json(json_updates)
        else:
            json_updates = await self._aio_post(self._get_api_url(method), payload)
            return Message._de_json(json_updates)

    def _get_api_url(self, method):
        return f"{self._api_url}{method}"

    def _get_file_url(self, path):
        return f"{self._file_url}{path}"

    async def _aio_post(self, url: str, payload: dict):
        resp = ""
        try:
            resp = await self._session.post(url, data=payload, timeout=None)
        except KeyboardInterrupt:
            quit()
        try:
            data = resp.json()
        except json.decoder.JSONDecodeError:
            raise TelegramConnectionError("Error: \n" + resp.text)

        if not data['ok']:
            raise TelegramConnectionError("Error: " + str(data["error_code"]) + " " + str(data['description']))

        return data['result']

    def _retrieve_updates(self, offset: int = None, limit: int = None, timeout: int = 20, allowed_updates: list = None, long_polling_timeout: int = 20):
        method = r'getUpdates'
        payload = {}
        if offset:
            payload['offset'] = offset
        if limit:
            payload['limit'] = limit
        if timeout:
            payload['timeout'] = timeout
        if long_polling_timeout:
            payload['long_polling_timeout'] = long_polling_timeout
        if allowed_updates:
            payload['allowed_updates'] = json.dumps(allowed_updates)
        url = self._get_api_url(method)
        try:
            update = self._loop.run_until_complete(self._aio_post(url, payload))
            results = []
            for u in update:
                results.append(Update._de_json(dict(u)))
            return results
        except KeyboardInterrupt:
            quit()

    async def get_updates(self, offset: int = None, limit: int = None, timeout: int = 20, allowed_updates: list = None, long_polling_timeout: int = 20):
        method = r'getUpdates'
        payload = {}
        if offset:
            payload['offset'] = offset
        if limit:
            payload['limit'] = limit
        if timeout:
            payload['timeout'] = timeout
        if long_polling_timeout:
            payload['long_polling_timeout'] = long_polling_timeout
        if allowed_updates:
            payload['allowed_updates'] = json.dumps(allowed_updates)
        url = self._get_api_url(method)
        update = await self._aio_post(url, payload)
        results = []
        for u in update:
            results.append(Update._de_json(dict(u)))
        return results

    def _get_bot(self):
        method = r'getMe'
        payload = {}
        url = self._get_api_url(method)
        return User._de_json(self._loop.run_until_complete(self._aio_post(url, payload)))

    def get_me(self):
        method = r'getMe'
        payload = {}
        url = self._get_api_url(method)
        return User._de_json(self._loop.run_until_complete(self._aio_post(url, payload)))

    async def forward_message(self, chat_id: int, from_chat_id: int, message_id: int, disable_notification: bool = False):
        method = r'forwardMessage'
        payload = {'chat_id': chat_id, 'from_chat_id': from_chat_id,
                   'message_id': message_id}

        if disable_notification:
            payload['disable_notification'] = disable_notification
        url = self._get_api_url(method)
        return Message._de_json(await self._aio_post(url, payload))

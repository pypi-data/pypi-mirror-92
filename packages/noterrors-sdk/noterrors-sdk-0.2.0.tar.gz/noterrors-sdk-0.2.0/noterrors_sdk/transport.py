import time
import base64
import asyncio

from .filetypes import FILETYPE

MAX_FILE_SIZE = 2 * 1 << 20


class TransportBase:
    _transport = None

    def __init__(self, address, project_token, auth_key):
        if address.endswith('/'):
            address = address[:-1]
        self.address = address
        self.project_token = project_token
        self.auth_key = auth_key
        self.headers = {
            'Project-Token': project_token,
            'Authenticate': auth_key
        }

    def prepare(self):
        raise NotImplementedError

    def prepare_message(self, message, message_type):
        files = message.get('attachments')
        if type(files) is dict:
            files = [files]
        elif not type(files) in (list, tuple):
            files = []
        attachments = []
        for file in files:
            if type(file) is dict:
                content = file.get('content')
                if type(content) is str:
                    content = content.encode('utf8')
                if len(content) < MAX_FILE_SIZE:
                    filetype = file.get('type') or FILETYPE.TEXT
                    if type(filetype) is not str:
                        filetype = filetype.value
                    attachments.append({
                        'name': file.get('name') or '',
                        'content': base64.b64encode(content).decode('utf8'),
                        'type': filetype,
                        'mimetype': file.get('mimetype')
                    })
        return {'type': message_type, 'send_time': time.time(), 'function': '', 'filename': '', **message, 'attachments': attachments}

    def capture_message(self, message, type='message'):
        raise NotImplementedError

    def save_copy(self, message, type):
        pass

    def clean_copy(self, copy_id):
        pass


class BasicTransport(TransportBase):
    def prepare(self):
        import requests, urllib3

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._transport = requests.Session()
        self._transport.verify = False

    def capture_message(self, message, type='message'):
        if self._transport is None:
            self.prepare()
        copy_id = self.save_copy(message, type)
        with self._transport.post(self.address + '/api/v1/events',
                              json=self.prepare_message(message, type),
                              headers=self.headers,
                              verify=False) as resp:
            if resp.status_code == 200:
                self.clean_copy(copy_id)


class AiohttpTransport(TransportBase):
    def prepare(self):
        import aiohttp

        self._transport = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))

    def capture_message(self, message, type='message'):
        asyncio.ensure_future(self._send_request(message, type))

    async def _send_request(self, message, type):
        if self._transport is None:
            self.prepare()
        copy_id = self.save_copy(message, type)
        async with self._transport.post(url=self.address + '/api/v1/events',
                                    json=self.prepare_message(message, type),
                                    headers=self.headers) as resp:
            if resp.status == 200:
                self.clean_copy(copy_id)


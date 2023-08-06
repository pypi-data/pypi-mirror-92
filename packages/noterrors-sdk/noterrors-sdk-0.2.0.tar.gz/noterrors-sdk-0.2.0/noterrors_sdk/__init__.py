import warnings
import traceback

from .client import NotErrorsClient
from .filetypes import FILETYPE


class NoterrorsSdk:
    _default_client = None
    _clients = {}
    _config = {}
    
    @classmethod
    def _get_client(cls, type=None):
        if type:
            client = cls._clients.get(type)
            if client is None:
                if not cls._config:
                    raise Exception('NotErrors SDK not initialized.')
                kwargs = cls._config['kwargs']
                kwargs['type'] = type
                client = cls._clients[type] = NotErrorsClient.init(*cls._config['args'], **kwargs)
        else:
            client = cls._default_client
        return client

    @classmethod
    def capture_message(cls, message, type=None, **kwargs):
        client = cls._get_client(type)
        if client:
            return client.capture_message(message, message_type='message', **kwargs)
        else:
            warnings.warn('NotErrors SDK is not configured.')

    @classmethod
    def handle_exception(cls, type=None, *args, **kwargs):
        try:
            client = cls._get_client(type)
            if client:
                return client.handle_exception(*args, **kwargs)
            else:
                warnings.warn('NotErrors SDK is not configured.')
        except Exception:
            tb = traceback.format_exc()
            print('NOTERRORS EXCEPTION:', tb)

    @classmethod
    def init(cls, *args, type='basic', **kwargs):
        cls._config = {'args': args, 'kwargs': {**kwargs, 'type': type}}
        cls._clients[type] = cls._default_client = NotErrorsClient.init(*args, type=type, **kwargs)


capture_message = NoterrorsSdk.capture_message
handle_exception = NoterrorsSdk.handle_exception
init = NoterrorsSdk.init


def noterrors_init(*args, type='basic', **kwargs):
    warnings.warn('"noterrors_init" is deprecated; use "init".', DeprecationWarning)
    init(*args, type=type, **kwargs)

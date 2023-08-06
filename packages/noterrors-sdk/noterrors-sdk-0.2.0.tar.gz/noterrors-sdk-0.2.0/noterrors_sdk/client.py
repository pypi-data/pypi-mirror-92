import os
import sys
import types
import socket
import atexit
import platform
import linecache
import importlib
import traceback

import noterrors_sdk.transport


class NotErrorsClient:
    origin_excepthook = sys.excepthook
    instance = False
    uname = platform.uname()

    def __init__(self, project_token, auth_key, type='basic', host=None):
        address = host or 'https://noterrors.com'
        Cls = getattr(noterrors_sdk.transport, type.capitalize() + 'Transport')
        self.transport = Cls(address, project_token, auth_key)

    @classmethod
    def init(cls, project_token, auth_key, type='basic', host=None):
        self = cls(project_token, auth_key, type, host)
        if not cls.instance:
            cls.instance = self
            sys.excepthook = cls.excepthook
        atexit.register(cls.sync_all)
        return self

    @classmethod
    def sync_all(cls):
        pass

    @classmethod
    def excepthook(cls, type, value, traceback):
        cls.instance._handle_exception(type, value, traceback, handled=False, level='error')
        cls.origin_excepthook(type, value, traceback)

    def _check_value(self, value):
        if isinstance(value, (types.ModuleType, types.FunctionType, types.BuiltinFunctionType, types.BuiltinMethodType)):
            return False
        try:
            if str(value).startswith('<class'):
                return False
        except Exception:
            return False
        return True

    def beautify(self, value):
        if value is None or isinstance(value, (int, float, bool)):
            return value
        if isinstance(value, str):
            return value[:300]
        if isinstance(value, (bytes, bytearray)):
            return value.decode(errors='ignore')[:300]
        if isinstance(value, (Exception,)):
            return str(value)
        return repr(value)

    def handle_exception(self, level=None, handled=True, **kwargs):
        ex_type, value, traceback = sys.exc_info()
        self._handle_exception(ex_type, value, traceback, level=level, handled=handled, **kwargs)

    def _handle_exception(self, ex_type, value, _tb=None, level=None, handled=True, **kwargs):
        if getattr(value, 'handled', None):
            return
        value.handled = True
        tb = _tb
        raw_stacktrace = ''.join(traceback.format_exception(ex_type, value, _tb))
        stacktrace = []
        while tb:
            frame = tb.tb_frame
            filename = frame.f_code.co_filename
            line = tb.tb_lineno
            code = linecache.getlines(filename)
            stacktrace.append({
                'method': frame.f_code.co_name,
                'package': frame.f_locals.get('__name__') or frame.f_globals.get('__name__'),
                'filename': filename,
                'line': line,
                'code': {
                    'before': code[line-6: line-1],
                    'line': code[line-1],
                    'after': code[line: line + 5],
                } if code else {},
                'vars': {n: self.beautify(v) for n, v in frame.f_locals.items() if not n.startswith('__') and self._check_value(v)}
            })
            tb = tb.tb_next
        if stacktrace:
            message = {
                'name': value.__class__.__name__,
                'title': str(value),
                'function': stacktrace[-1]['method'],
                'filename': stacktrace[-1]['filename'],
                'package': stacktrace[-1]['package'],
                'stacktrace': stacktrace,
                'raw_stacktrace': raw_stacktrace,
                'level': level,
                'tags': {
                    'level': level,
                    'handled': handled
                },
                'meta': {
                    'handled': handled,
                    'extra': {
                        'argv': sys.argv
                    }
                }
            }
            self.capture_message(message, message_type='error', **kwargs)

    def capture_message(self, message, message_type='message', attachments=None, tags=None, meta=None):
        if type(message) is str:
            message = {
                'name': 'User message',
                'title': message
            }

        message.update({
            'meta': message.get('meta') or {},
            'attachments': attachments,
            'user_tags': tags,
            'platform': 'python',
            'environment': {
                'system': self.uname.system,
                'release': self.uname.release,
                'os_version': self.uname.version,
                'machine': self.uname.machine,
                'runtime': sys.version,
                'platform': sys.platform,
                'hostname': self.uname.node,
                'username': os.getlogin(),
                'os_release':  platform.release(),
                'ip_address': socket.gethostbyname(socket.gethostname())
            }
        })
        if meta:
            message['meta'].update(meta)

        # TODO: delayed queues
        # payload = {
        #     'items': [message]
        # }
        self.transport.capture_message(message, message_type)

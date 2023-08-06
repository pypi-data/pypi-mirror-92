from functools import partial

from flask import request, __version__
import noterrors_sdk


class NoterrorsFlask:
    def __init__(self, app):
        self.init_app(app)
        noterrors_sdk.init(**app.config['NOTERRORS_CONFIG'])

    def init_app(self, app):
        app.handle_exception = partial(self.error_router, app.handle_exception)
        app.handle_user_exception = partial(self.error_router, app.handle_user_exception)

    def error_router(self, origin, exception):
        tags = {
            'url': request.url,
            'method': request.method,
            'flask': __version__
        }
        noterrors_sdk.handle_exception(tags=tags)
        return origin(exception)

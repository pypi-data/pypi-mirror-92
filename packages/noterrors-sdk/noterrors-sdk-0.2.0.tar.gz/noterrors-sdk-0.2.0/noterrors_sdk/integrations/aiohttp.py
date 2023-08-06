from aiohttp import web, __version__
import noterrors_sdk


@web.middleware
async def noterrors_middleware(request, handler):
    try:
        return await handler(request)
    except Exception as ex:
        tags = {
            'url': request.url,
            'method': request.method,
            'aiohttp': __version__
        }
        noterrors_sdk.handle_exception(tags=tags)
        raise ex


def noterrors_aiohttp_middleware(**config):
    noterrors_sdk.init(**config)

    return noterrors_middleware

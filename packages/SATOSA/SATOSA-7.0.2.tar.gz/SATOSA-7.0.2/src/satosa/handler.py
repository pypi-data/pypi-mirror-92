import io

from saml2.s_utils import UnknownSystemEntity

from satosa.base import SATOSABase
from satosa.context import Context
from satosa.logging import getLogger
from satosa.routing import SATOSANoBoundEndpointError

from .request import unpack_request
from .response import NotFound
from .response import ServiceError


logger = getLogger(__name__)


class Application(SATOSABase):
    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "").lstrip("/")
        if ".." in path or path == "":
            resp = NotFound("Couldn't find the page you asked for!")
            return resp(environ, start_response)

        context = Context()
        context.path = path

        # copy wsgi.input stream to allow it to be re-read later by satosa plugins
        # see: http://stackoverflow.com/questions/1783383/how-do-i-copy-wsgi-input-if-i-want-to-process-post-data-more-than-once
        content_length = int(environ.get("CONTENT_LENGTH") or "0")
        body = io.BytesIO(environ["wsgi.input"].read(content_length))
        environ["wsgi.input"] = body
        context.request = unpack_request(environ, content_length)
        environ["wsgi.input"].seek(0)

        context.cookie = environ.get("HTTP_COOKIE", "")
        context.request_authorization = environ.get("HTTP_AUTHORIZATION", "")

        try:
            resp = self.run(context)
            if isinstance(resp, Exception):
                raise resp
        except SATOSANoBoundEndpointError:
            resp = NotFound(
                "The Service or Identity Provider you requested could not be found."
            )
        except Exception as e:
            if type(e) != UnknownSystemEntity:
                logger.exception(e)
            resp = ServiceError(str(e))

        return resp(environ, start_response)

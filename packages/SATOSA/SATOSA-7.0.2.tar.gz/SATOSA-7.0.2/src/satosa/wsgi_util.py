from functools import reduce
from functools import partial
from logging.config import dictConfig as configure_logging_by_dict

from cookies_samesite_compat import CookiesSameSiteCompatMiddleware

import satosa
from satosa.logging import getLogger
from satosa.functional import compose
from satosa.network.handler import Application
from satosa.network.middleware import DataToBytes
from satosa.network.middleware import DataToList
from satosa.network.middleware import Base  # XXX


logger = getLogger(__name__)


def make_app(config):
    logging_config = config.get("LOGGING", {"version": 1})
    configure_logging_by_dict(logging_config)
    logger.info("Running SATOSA version {v}".format(v=satosa.__version__))

    try:
        handler = Application(config)
        middlewares = [
            partial(DataToList, config=config),
            partial(DataToBytes, config=config),
            partial(CookiesSameSiteCompatMiddleware, config=config),
            partial(Base, config=config),
        ]
        app = reduce(compose, middlewares, handler)
    except Exception:
        logline = "Failed to create WSGI app."
        logger.exception(logline)
        raise

    return app

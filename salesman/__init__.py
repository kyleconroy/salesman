from gevent import monkey
monkey.patch_all()

import os
import logging
import logging.config
from gevent.pool import Pool
from lxml import etree
from restkit import request
from restkit.globals import set_manager
from restkit.manager.mgevent import GeventManager
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse

# set the gevent connection manager
set_manager(GeventManager(timeout=200))


def url_join(base, link):
    if urlparse(link).netloc:
        return link

    join = urljoin(base, link)
    url = urlparse(join)
    path = os.path.normpath(url.path)
    # Strip hashes, bug in restkit

    return urlunparse(
        (url.scheme, url.netloc, path, url.params, url.query, None)
        )


def get_urls(base, html):
    """Given a string of html, return all the urls that are linked
    """
    tree = etree.HTML(html)
    links = tree.iterfind(".//a[@href]")
    return [url_join(base, a.attrib["href"].strip()) for a in links]


LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "salesman": {
            "format": ("[%(levelname)s] - %(status)s %(url)s "
                       "%(source)s %(message)s"),
        },
        "pretty-salesman": {
            "format": ("%(levelname)s\tHTTP %(status)s\nURL\t%(url)s\nSOURCE"
                       "\t%(source)s\n\n"),
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "salesman",
            "filename": "travel.log",
        },
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "pretty-salesman",
            "stream": "ext://sys.stderr"
        },
    },
    "loggers": {
        "salesman": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
        },
    }
}


class Salesman(object):

    def __init__(self, externals=False, logger=None, log_config=None):
        """
        :param externals: If True, check that links to external URLs are valid
        :param logger: The logger to use
        :param log_config: The log_config dictionary to use
        :param verbose: If true, print out errors to stderror
        """
        if log_config is None:
            log_config = LOG_CONFIG

        if logger is not None:
            self.logger = logger
        else:
            logging.config.dictConfig(log_config)
            self.logger = logging.getLogger("salesman")

        self.externals = externals
        self.visited_urls = set()
        self.next_urls = []

    def verify(self, *vurls):
        for url in vurls:
            self.base = urlparse(url)
            urls = self.visit(url)

            # Limit Pool size to 100 to prevent HTTP timeouts
            pool = Pool(100)

            def visit(url, source):
                if not self.is_invalid(url):
                    self.visit(url, source)

            for vurl, source in urls:
                pool.spawn(visit, vurl, source)
            pool.join()

    def visit(self, url, source=None):
        """ Visit the url and return the response
        :return: The set of urls on that page
        """
        self.visited_urls.add(url)

        try:
            response = request(url, follow_redirect=True)
        except Exception as e:
            return []

        # Rest the url for redirects
        url = response.final_url

        # Add the new url to the set as well
        self.visited_urls.add(url)

        o = urlparse(url)
        level = logging.INFO if response.status_int < 400 else logging.ERROR
        plans = "VISIT" if o.netloc == self.base.netloc else "STOP"

        d = {
            "status": response.status,
            "url": url,
            "source": source,
            }

        self.logger.log(level, "%s", plans, extra=d)

        if o.netloc != self.base.netloc:
            return []

        try:
            return [(u, url) for u in get_urls(url, response.body_string())]
        except Exception as e:
            return []

    def is_invalid(self, url):
        return (url in self.visited_urls
                or url.startswith("mailto:")
                or url.startswith("javascript:"))

    def explore(self, url):
        """Travel will never stop"""
        self.visited_urls = set()
        self.base = urlparse(url)

        # Limit Pool size to 100 to prevent HTTP timeouts
        pool = Pool(100)

        def visit(target, source):
            if not self.is_invalid(target):
                for url, source in self.visit(target, source):
                    pool.apply_async(visit, args=[url, source])

        pool.apply_async(visit, args=[url, None])
        pool.join()

import os
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse


def url_join(base, link):
    join = urljoin(base, link)
    url = urlparse(join)
    path = os.path.normpath(url.path)
    return urlunparse(
        (url.scheme, url.netloc, path, url.params, url.query, url.fragment)
        )

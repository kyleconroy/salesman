import os
import logging
from lxml import etree
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse

def url_join(base, link):
    if urlparse(link).netloc:
        return link

    join = urljoin(base, link)
    url = urlparse(join)
    path = os.path.normpath(url.path)
    return urlunparse(
        (url.scheme, url.netloc, path, url.params, url.query, url.fragment)
        )

def get_urls(base, html):
    """Given a string of html, return all the urls that are linked
    """
    tree = etree.HTML(html)
    links = tree.iterfind(".//a[@href]")
    return [url_join(base, a.attrib["href"]) for a in links]


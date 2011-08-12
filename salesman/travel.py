import gevent
from gevent import monkey; monkey.patch_all()

import requests
import urlparse
import logging
from argparse import ArgumentParser
from gevent.pool import Pool
from salesman import get_urls

logging.basicConfig(filename='travel.log', level=logging.DEBUG)

parser = ArgumentParser(description="Check all links")
parser.add_argument("url", type=str, help="First URL to visit")
args = parser.parse_args()

base = urlparse.urlparse(args.url)
visited_urls = set()
next_urls = [(args.url, "")]

def visit(url, source):
    if url in visited_urls:
        return

    o = urlparse.urlparse(url)
    visited_urls.add(url)

    try:
        response = requests.get(url)
    except:
        return

    level = logging.INFO if response.ok else logging.ERROR
    plans = "VISIT" if o.netloc == base.netloc else "STOP"
    #log = [str(response.status_code), plans, url]

    logging.log(level, "%s %s %s", response.status_code, url, source)

    if o.netloc == base.netloc:
        try:
            urls = [(u, url) for u in get_urls(url, response.content)]
            next_urls.extend(urls)
        except:
            pass

while next_urls:
    pool = Pool(50)
    for url, source in next_urls:
        pool.spawn(visit, url, source)
    pool.join()

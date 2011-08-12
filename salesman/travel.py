import gevent
from gevent import monkey; monkey.patch_all()

import requests
import urlparse
import logging
from argparse import ArgumentParser
from gevent.pool import Pool
from salesman import get_urls

parser = ArgumentParser(description="Check all links")
parser.add_argument("url", type=str, help="First URL to visit")
args = parser.parse_args()

base = urlparse.urlparse(args.url)
visited_urls = set()
next_urls = [(args.url, "")]

pool = Pool(50)

def visit(url):
    if url in visited_urls:
        return

    o = urlparse.urlparse(url)
    visited_urls.add(url)

    try:
        response = requests.get(url)
    except:
        print ", ".join([BAD_URL, 600, plans, url])

    status = "OK" if response.ok else "FAIL"
    plans = "VISIT" if o.netloc == base.netloc else "STOP"
    log = [status, str(response.status_code), plans, url]

    if response.ok:
        logging.info(*log)
    else:
        logging.error(*log)

    if o.netloc == base.netloc:
        try:
            next_urls.extend(get_urls(url, response.content))
        except:
            ## Failed HTML parsing
            pass

visit(args.url)

while next_urls:
    for url in next_urls:
        pool.spawn(visit, url)
    pool.join()


import os
from argparse import ArgumentParser
from salesman import Salesman


def main():
    parser = ArgumentParser(description="Check all links")
    parser.add_argument("action", type=str, choices=["visit", "explore"],
                        help=("What action Salesman should take"))
    parser.add_argument("url", type=str, help="Absolute URL")
    args = parser.parse_args()

    willy_lowman = Salesman()

    print "Traveling your website. This could take O(n^2*2^n) time"

    if args.action == "visit":
        if os.path.isfile(args.url):
            urls = open(args.url).readlines()
            willy_lowman.verify(*urls)
        else:
            willy_lowman.verify(args.url)
    else:
        willy_lowman.explore(args.url)

    print "Tested {} urls".format(len(willy_lowman.visited_urls))

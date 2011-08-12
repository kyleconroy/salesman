from nose.tools import assert_equals
from salesman import url_join

urls = [
    ("http://www.google.com/", "docs", "http://www.google.com/docs"),
    ("http://www.google.com/#bar", "docs", "http://www.google.com/docs"),
    ("http://www.google.com/foo", "docs", "http://www.google.com/docs"),
    ("http://www.google.com/foo#bar", "docs", "http://www.google.com/docs"),
    ("http://www.google.com/foo#bar", "docs?hey=you",
     "http://www.google.com/docs?hey=you"),
    ("http://www.google.com/foo#bar", "docs?hey=you#foo",
     "http://www.google.com/docs?hey=you#foo"),
    #("http://www.google.com/foo/bar", ".", "http://www.google.com/foo/"),
    ("http://www.google.com/foo", "..", "http://www.google.com/"),
    ("http://www.google.com/foo", "../..", "http://www.google.com/"),
    ("http://www.google.com/foo", "./../..", "http://www.google.com/"),
    ("http://www.google.com/foo", "../../..", "http://www.google.com/"),
    ("http://www.google.com/foo", "..", "http://www.google.com/"),
    ("http://www.google.com/foo", "../..", "http://www.google.com/"),
    ("http://www.google.com/foo", "../../..", "http://www.google.com/"),
    ("http://www.google.com/foo/bar/baz", "/", "http://www.google.com/"),
    #("http://www.google.com/foo/bar/baz", "..", "http://www.google.com/foo/"),
    #("http://www.google.com/foo/bar/baz", "../", "http://www.google.com/foo/"),
    ("http://www.google.com/foo/bar/baz", "../bar", "http://www.google.com/foo/bar"),
    ('http://site.com/', '/path/../path/.././path/./', "http://site.com/path"),
    ('http://site.com/path/x.html', '/path/../path/.././path/./y.html',
     "http://site.com/path/y.html"),
    ('http://site.com/', '../../../../path/', "http://site.com/path"),
    ('http://site.com/x/x.html', '../../../../path/moo.html',
     "http://site.com/path/moo.html"),
    ('http://site.com/99/x.html', '1/2/3/moo.html',
     "http://site.com/99/1/2/3/moo.html"),
    ('http://site.com/99/x.html', '../1/2/3/moo.html',
     "http://site.com/1/2/3/moo.html"),
    ]

def check_url_join(base, link, expected):
    assert_equals(url_join(base, link), expected)

def test_url_join():
    for base, link, expected in urls:
        yield check_url_join, base, link, expected



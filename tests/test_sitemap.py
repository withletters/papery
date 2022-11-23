# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from nose.tools import eq_

from papery.sitemap import Sitemap


def test_sitemap():

    reference = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

    <url>
        <loc>http://www.example.com/</loc>
        <lastmod>1970-01-01T00:00:00Z</lastmod>
    </url>

</urlset>"""

    # path = '/tmp/sitemap.xml'

    pages = [{'location': "http://www.example.com/",
              'modified': 0}]

    sitemap = Sitemap(pages)

    eq_(reference, sitemap.content, "Not match")

# -*- coding: utf-8 -*-
#
# Copyright (C) 2013, Xcoo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import absolute_import
from __future__ import print_function, unicode_literals

import jinja2
from jinja2 import Template

import codecs
import os
import time
import gzip


class Sitemap(object):

    def __init__(self, pages):

        self.template_env = jinja2.Environment()
        self.template_env.filters.update({"timestamp": timestamp})

        self.pages = pages

        self.template_path = os.path.join(os.path.dirname(__file__),
                                          'sitemap_template.xml')

        with codecs.open(self.template_path, 'r', encoding="utf-8") as fp:
            template_text = fp.read()
            fp.close()

        self.template = self.template_env.from_string(template_text)

    def save(self, path):
        content = self.content

        with codecs.open(path, 'w', encoding="utf-8") as fp:
            fp.write(content)

        with gzip.open(path + '.gz', 'wb') as gzfp:
            gzfp.write(content.encode('utf-8'))

    @property
    def content(self):
        return self.template.render(pages=self.pages)


def timestamp(t):
    """Seconds since epoch (1970-01-01) --> ISO 8601 time string."""
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t))

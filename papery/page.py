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
import markdown2
import json
import codecs


class Post(object):

    def __init__(self, filepath):
        self.filepath = filepath

    def text(self, lang):

        # TODO(takashi) switch with language

        fp = codecs.open(self.filepath, 'r', encoding="utf-8")
        text = fp.read()
        fp.close()
        return markdown2.Markdown().convert(text)


class Page(object):

    def __init__(self, template_dir=".", template_name="default.tmpl",
                 post_file_name="default.md",
                 info_file_name="default.json"):
        loader = jinja2.FileSystemLoader(template_dir)
        self.template_env = jinja2.Environment(loader=loader)
        self.template_env.filters.update({"linebreaksbr": linebreaksbr})

        self.template_name = template_name
        self.post_file_name = post_file_name
        self.info_file_name = info_file_name

    def render(self):
        self.template = self.template_env.get_template(self.template_name)

        try:
            with open(self.info_file_name) as info_file:
                info = json.load(info_file)
        except IOError:
            print("Not found info file %s" % self.info_file_name)
            info = {}

        post = Post(self.post_file_name)

        return self.template.render({"info": info, "post": post})


def linebreaksbr(arg):
    return arg.replace("\n", "<br />\n")

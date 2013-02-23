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

import os
import sys
import glob
import codecs

from papery.page import Page


class Renderer(object):

    def __init__(self, config, output_dir="output"):
        self.config = config
        self.output_dir = output_dir

        if "theme" not in self.config:
            self.config["theme"] = "default"

        if "pages" not in self.config:
            self.pages = [{"file": "pages/*.md",
                           "template": "page.tmpl"}]

        self._targets = {}

    def run(self):
        self._check()
        self._prepare_output()
        self._scan()
        self._render_pages()

    def _check(self):
        theme_path = os.path.join("themes", self.config["theme"])
        theme_templates_path = os.path.join(theme_path, "templates")
        theme_assets_path = os.path.join(theme_path, "assets")

        if not os.path.isdir(theme_path):
            # logging.critical("This doesn't look like a wok site. Aborting.")
            print("Not found theme directory %s. Aborting." %
                  theme_path)
            sys.exit(1)

        if not os.path.isdir(theme_templates_path):
            print("Not found theme templates directory %s. Aborting." %
                  theme_templates_path)
            sys.exit(1)

        if not os.path.isdir(theme_assets_path):
            print("Not found theme assets directory %s. Aborting." %
                  theme_templates_path)
            sys.exit(1)

        for page in self.config["pages"]:
            page_dirpath = os.path.dirname(page["file"])

            if not os.path.isdir(page_dirpath):
                print("Not found page directory %s. Aborting." %
                      page_dirpath)
                sys.exit(1)

    def _prepare_output(self):
        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

    def _scan(self):
        for page in self.config["pages"]:
            page_dirpath = os.path.dirname(page["file"])
            page_basename = os.path.basename(page["file"])
            for dirpath, _, _ in os.walk(page_dirpath):
                match = os.path.join(dirpath, page_basename)
                for p in glob.glob(match):
                    self._targets[p] = page["template"]

    def _render_pages(self):
        theme_path = os.path.join("themes", self.config["theme"])
        theme_templates_path = os.path.join(theme_path, "templates")

        for page, template in self._targets.items():
            print("rendering %s" % page)
            page_base, _ = os.path.splitext(page)
            info = page_base + ".json"
            page_name = os.path.basename(page_base)
            p = Page(template_dir=theme_templates_path, template_name=template,
                     post_file_name=page, info_file_name=info)

            output_filename = page_name + ".html"
            output_file_path = os.path.join(self.output_dir, output_filename)
            fp = codecs.open(output_file_path, 'w', encoding="utf-8")
            fp.write(p.render())
            fp.close()

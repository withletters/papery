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
import shutil

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin  # NOQA

from papery.page import Page
from papery.sitemap import Sitemap
from papery.util import weak_tree_copy


class Renderer(object):

    def __init__(self, config, output_dir="output"):
        self.config = config
        self.output_dir = output_dir

        if "theme" not in self.config:
            self.config["theme"] = "default"

        if "pages" not in self.config:
            self.pages = [{"file": "pages/*.md",
                           "template": "page.tmpl",
                           "path": "/"}]

        self._targets = {}
        self._page_maps = []

    def run(self):
        self._check()
        self._prepare_output()
        self._scan()
        self._render_pages()
        self._copy_assets()
        self._generate_sitemap()

    def clean(self):
        self._check()
        self._remove_output()

    def _remove_output(self):
        if os.path.isdir(self.output_dir):
            shutil.rmtree(self.output_dir)

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

        for p in self.config["pages"]:
            if 'path' in p:
                path = p['path']

                if path.startswith('/'):
                    path = path[1:]

                path = os.path.join(self.output_dir, path)

                if not os.path.isdir(path):
                    os.makedirs(path)

    def _scan(self):
        for page in self.config["pages"]:
            page_dirpath = os.path.dirname(page["file"])
            page_basename = os.path.basename(page["file"])

            page_output_dirpath = ""

            if 'path' in page:
                path = page['path']

                if path.startswith('/'):
                    path = path[1:]

                page_output_dirpath = path

            for dirpath, _, _ in os.walk(page_dirpath):
                match = os.path.join(dirpath, page_basename)
                for p in glob.glob(match):
                    self._targets[p] = {'template': page['template'],
                                        'path': page_output_dirpath}

    def _render_pages(self):
        theme_path = os.path.join("themes", self.config["theme"])
        theme_templates_path = os.path.join(theme_path, "templates")

        for page, render_vars in self._targets.items():
            page_base, _ = os.path.splitext(page)
            info = page_base + ".json"
            page_name = os.path.basename(page_base)
            p = Page(template_dir=theme_templates_path,
                     template_name=render_vars['template'],
                     post_file_name=page, info_file_name=info)

            output_filename = page_name + ".html"

            output_file_path = os.path.join(self.output_dir,
                                            render_vars['path'],
                                            output_filename)

            if not os.path.exists(output_file_path) or os.path.getmtime(output_file_path) < p.mtime:
                if os.path.exists(output_file_path):
                    os.remove(output_file_path)

                print("rendering %s" % page)

                text = p.render()

                if text is not None:
                    with codecs.open(output_file_path, 'w', encoding="utf-8") as fp:
                        fp.write(text)

            self._page_maps.append({'location': output_filename,
                                    'modified': p.mtime})

    def _copy_assets(self):
        theme_path = os.path.join("themes", self.config["theme"])
        theme_assets_path = os.path.join(theme_path, "assets")

        page_assets_path = os.path.join("files", "assets")

        output_assets_dir = os.path.join(self.output_dir, "assets")

        if not os.path.isdir(output_assets_dir):
            os.mkdir(output_assets_dir)

        weak_tree_copy(theme_assets_path, output_assets_dir)
        weak_tree_copy(page_assets_path, output_assets_dir)

        robots_txt_path = os.path.join("files", "robots.txt")
        output_robots_txt_path = os.path.join(self.output_dir, "robots.txt")

        if os.path.exists(robots_txt_path):
            if not os.path.exists(output_robots_txt_path) or os.path.getmtime(output_robots_txt_path) < os.path.getmtime(robots_txt_path):
                print("cp %s %s" % (robots_txt_path, output_robots_txt_path))
                shutil.copy(robots_txt_path, output_robots_txt_path)
                shutil.copystat(robots_txt_path, output_robots_txt_path)

    def _generate_sitemap(self):

        if 'url' in self.config:
            site_url = self.config['url']
        else:
            site_url = '/'

        for p in self._page_maps:
            p['location'] = urljoin(site_url, p['location'])

        sitemap = Sitemap(self._page_maps)
        path = os.path.join(self.output_dir, 'sitemap.xml')
        sitemap.save(path)

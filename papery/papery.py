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

import papery.serving
import papery.rendering

from papery.util import weak_tree_copy


class Papery(object):

    def __init__(self, config={}):
        self.config = config

        if 'papery' in config:
            c = config['papery']

            self.output_dir = c['output'] if 'output' in c else 'output'
            self.themes_dir = c['themes'] if 'themes' in c else 'themes'
            self.files_dir = c['files'] if 'files' in c else 'files'
        else:
            self.output_dir = 'output'
            self.themes_dir = 'themes'
            self.files_dir = 'files'

    def render(self, **args):
        renderer = papery.rendering.Renderer(self.config,
                                             self.themes_dir,
                                             self.files_dir,
                                             self.output_dir)
        renderer.run()

    def run_server(self, **args):
        self.render()

        watch_dirs = []

        theme_path = os.path.join(self.themes_dir, self.config["theme"])
        watch_dirs.append(os.path.abspath(theme_path))

        for page in self.config["pages"]:
            page_dirpath = os.path.dirname(page["file"])
            watch_dirs.append(os.path.abspath(page_dirpath))

        server = papery.serving.Server(root_dir=self.output_dir,
                                       watch_dirs=watch_dirs,
                                       change_handler=self.rebuild)
        server.run()

    def rebuild(self):
        self.render()

    def clean(self, **args):
        renderer = papery.rendering.Renderer(self.config,
                                             self.themes_dir,
                                             self.files_dir,
                                             self.output_dir)
        renderer.clean()

    def initialize(self, **args):
        sample_dir_path = os.path.join(os.path.dirname(__file__),
                                       'data', 'sample')

        weak_tree_copy(sample_dir_path, '.',
                       overwrite_if_modified=False)

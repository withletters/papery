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


class Papery(object):

    def __init__(self, config={}):
        self.config = config

    def render(self, **args):
        renderer = papery.rendering.Renderer(self.config)
        renderer.run()

    def run_server(self, **args):
        self.render()

        watch_dirs = []

        theme_path = os.path.join("themes", self.config["theme"])
        watch_dirs.append(os.path.abspath(theme_path))

        for page in self.config["pages"]:
            page_dirpath = os.path.dirname(page["file"])
            watch_dirs.append(os.path.abspath(page_dirpath))

        server = papery.serving.Server(root_dir="output",
                                       watch_dirs=watch_dirs,
                                       change_handler=self.rebuild)
        server.run()

    def rebuild(self):
        self.render()

    def clean(self, **args):
        renderer = papery.rendering.Renderer(self.config)
        renderer.clean()

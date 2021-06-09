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

import re

import jinja2
from jinja2 import meta

import markdown2
import json
import yaml
import codecs

import os


class Post(object):

    def __init__(self, filepath):
        self.filepath = filepath

    def _build_link(self, text):
        return re.sub("<a.*?href=\"(.+?)\".*?>(.+?)</a>",
                      "<a href=\"\\1\" target=\"_blank\">\\2</a>",
                      text)

    def text(self, lang=None, link=None):

        # TODO(takashi) switch with language

        fp = codecs.open(self.filepath, 'r', encoding="utf-8")
        text = fp.read()
        fp.close()

        if link is None:
            text = markdown2.markdown(text, extras=["tables"])
            return markdown2.Markdown().convert(text)
        else:
            return self._build_link(markdown2.Markdown().convert(text))


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

        self.template = self.template_env.get_template(self.template_name)

        self.sub_file_names = self._scan_info()

    def render(self,
               author='', title='',
               url='', email='', keywords='', description='',
               variables={}):
        if self.info_file_name.endswith('.yaml'):
            try:
                with codecs.open(self.info_file_name, 'r', encoding="utf-8") as info_file:
                    info = yaml.safe_load(info_file)
            except IOError:
                print("Not found info file %s" % self.info_file_name)
                info = {}
            except ValueError as e:
                print("YAML Parse error in %s" % self.info_file_name)
                print(e.args[0])
                return None
        else:
            try:
                with codecs.open(self.info_file_name, 'r', encoding="utf-8") as info_file:
                    info = json.load(info_file)
            except IOError:
                print("Not found info file %s" % self.info_file_name)
                info = {}
            except ValueError as e:
                print("JSON Parse error in %s" % self.info_file_name)
                print(e.args[0])
                return None

        post = Post(self.post_file_name)

        render_vars = variables
        info = self._build_info(info)

        render_vars.update(info)
        render_vars.update({"post": post})

        if 'author' not in render_vars or len(render_vars['author']) == 0:
            render_vars['author'] = author

        if 'title' not in render_vars or len(render_vars['title']) == 0:
            render_vars['title'] = title

        if 'url' not in render_vars or len(render_vars['url']) == 0:
            render_vars['url'] = url

        if 'email' not in render_vars or len(render_vars['email']) == 0:
            render_vars['email'] = email

        if 'keywords' not in render_vars or len(render_vars['keywords']) == 0:
            render_vars['keywords'] = keywords

        if 'description' not in render_vars or len(render_vars['description']) == 0:
            render_vars['description'] = description

        return self.template.render(render_vars)

    @property
    def mtime(self):
        template_mtime = self._template_mtime()

        if os.path.exists(self.post_file_name):
            post_mtime = os.path.getmtime(self.post_file_name)
        else:
            post_mtime = 0

        if os.path.exists(self.info_file_name):
            info_mtime = os.path.getmtime(self.info_file_name)
        else:
            info_mtime = 0

        mtimes = [template_mtime, post_mtime, info_mtime]

        for f in self.sub_file_names:
            if os.path.exists(f):
                mtimes.append(os.path.getmtime(f))

        return max(mtimes)

    def _template_mtime(self):
        mtimes = []

        mtimes.append(os.path.getmtime(self.template.filename))

        with codecs.open(self.template.filename, 'r', encoding="utf-8") as fp:
            text = fp.read()
            fp.close()

        ast = self.template_env.parse(text)
        refs = list(meta.find_referenced_templates(ast))

        while len(refs) > 0:
            r = refs.pop()
            t = self.template_env.get_template(r)

            with codecs.open(t.filename, 'r', encoding="utf-8") as fp:
                text = fp.read()
                fp.close()

            mtimes.append(os.path.getmtime(t.filename))

            ast = self.template_env.parse(text)
            refs.extend(list(meta.find_referenced_templates(ast)))

        return max(mtimes)

    md_re = re.compile("^md\((.+?)\)$")

    def _scan_info(self):
        if self.info_file_name.endswith('.yaml'):
            try:
                with codecs.open(self.info_file_name, 'r', encoding="utf-8") as info_file:
                    info = yaml.safe_load(info_file)
            except IOError:
                info = {}
            except ValueError as e:
                print("YAML Parse error in %s" % self.info_file_name)
                print(e.args[0])
                info = {}
        else:
            try:
                with codecs.open(self.info_file_name, 'r', encoding="utf-8") as info_file:
                    info = json.load(info_file)
            except IOError:
                info = {}
            except ValueError as e:
                print("JSON Parse error in %s" % self.info_file_name)
                print(e.args[0])
                info = {}

        return self.__scan_info(info)

    def __scan_info(self, info):
        files = []

        if type(info) is dict:
            for k in info:
                files.extend(self.__scan_info(info[k]))

        elif type(info) is list:
            for v in info:
                files.extend(self.__scan_info(v))

        elif type(info) is str or type(info) is unicode:
            m = self.md_re.match(info)

            if m is not None:
                path = m.groups()[0]
                path = os.path.join(os.path.dirname(self.info_file_name), path)

                files.append(path)

        return files

    def _build_info(self, info):

        if type(info) is dict:
            for k in info:
                info[k] = self._build_info(info[k])

            return info
        elif type(info) is list:
            newval = []

            for v in info:
                newval.append(self._build_info(v))

            info = newval

            return info
        elif type(info) is str or type(info) is unicode:
            m = self.md_re.match(info)

            if m is None:
                return info
            else:
                path = m.groups()[0]
                path = os.path.join(os.path.dirname(self.info_file_name), path)

                post = Post(path)
                return post
        else:
            return info


def linebreaksbr(arg):
    return arg.replace("\n", "<br />\n")

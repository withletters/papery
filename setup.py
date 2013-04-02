#!/usr/bin/env python
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


from setuptools import setup

setup(
    name="papery",
    version="0.1.0",
    description="Static Web Generator",
    long_description=__doc__,
    license="Apache License 2.0",
    author="Xcoo, Inc.",
    author_email="developer@xcoo.jp",
    url="https://github.com/withletters/papery",
    install_requires=["jinja2", "markdown2"],
    packages=['papery'],
    package_data={'papery': ['sitemap_template.xml']},
    scripts=['scripts/papery'])

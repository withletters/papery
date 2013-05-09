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

from papery import version
from papery.papery import Papery

import json
import os
import sys
import argparse
#import logging


class Engine(object):

    def __init__(self):

        parser = argparse.ArgumentParser()

        parser.add_argument('--version', action='version', version=version)

        subparsers = parser.add_subparsers(help='sub-command help',
                                           dest='command')

        parser_build = subparsers.add_parser('build',
                                             help='build site')
        parser_build.add_argument('--debug',
                                  type=int,
                                  help='output debug log')

        parser_run = subparsers.add_parser('run',
                                           help='run development server')
        parser_run.add_argument('--debug',
                                type=int,
                                help='output debug log')

        parser_init = subparsers.add_parser('init',
                                            help='initialize site')
        parser_init.add_argument('--debug',
                                 type=int,
                                 help='output debug log')

        parser_clean = subparsers.add_parser('clean',
                                             help='clear all')

        parser_clean.add_argument('--debug',
                                  type=int,
                                  help='output debug log')

        args = parser.parse_args()

        try:
            config_path = ''

            if os.path.exists('config.json'):
                config_path = 'config.json'
            elif os.path.exists('.config.json'):
                config_path = '.config.json'

            with open(config_path) as config_file:
                config = json.load(config_file)
                self.site = Papery(config)
        except IOError:
            print('Not found \"config.json\". Papery run with default configuration.',
                  file=sys.stderr)
            self.site = Papery()

        if args.command == 'build':
            self.site.render(**args.__dict__)
        elif args.command == 'run':
            self.site.run_server(**args.__dict__)
        elif args.command == 'init':
            self.site.initialize(**args.__dict__)
        elif args.command == 'clean':
            self.site.clean(**args.__dict__)

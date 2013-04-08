Papery version 0.1.3

# Papery

papery is  is a simple, static site generator written in Python - supports Markdown/JSON input and Jinja2 templating.

# Features

- Markdown and JSON as input.
- Jinja2 templating.
- Python 2 and 3 compatible.
- Embed development web server (automatic updating)

# Requirements

- [Jinja2](http://jinja.pocoo.org/)
- [markdown2](https://github.com/trentm/python-markdown2)

# Installation

papery is available on [pypi](https://pypi.python.org/pypi).
To get the latest released version:

    pip install papery

# Usage

## Creating new site

Run the following command

    cd path/to/your_site
    papery init

## Run with development server

    papery run

access to <http://localhost:8000> with your web browser.

All pages are automatically updated when you modified any resources.

## Build manually

    papery build

# TODO

- documentation
- validate Markdown/JSON syntax
- code syntax highlight
- create new pages via papery sub command

# License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

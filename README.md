[![PyPI version](https://badge.fury.io/py/papery.svg)](https://badge.fury.io/py/papery)

# Papery

Static site generator with Jinja2 templates and structured content in Markdown, YAML, and JSON

## Features

- Describe content with Markdown, YAML, and JSON
- Jinja2 templating

## Requirements

- Python 3.9+
- [Jinja2](https://jinja.palletsprojects.com/)
- [markdown](https://github.com/Python-Markdown/markdown)
- [pymdown-extensions](https://github.com/facelessuser/pymdown-extensions)
- [Pygments](https://pygments.org/)
- [pyyaml](https://pypi.org/project/PyYAML/)
- [yamllint](https://github.com/adrienverge/yamllint)
- [pykwalify](https://github.com/Grokzen/pykwalify)

The following Node.js tools are optional. If installed, they are used for validation.

- [jsonlint](https://github.com/zaach/jsonlint) (`npm install -g jsonlint`)
- [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli) (`npm install -g markdownlint-cli`)

## Installation

Papery is available on [pypi](https://pypi.python.org/pypi).

```console
pip install papery
```

or, with [uv](https://docs.astral.sh/uv/):

```console
uv tool install papery
```

## Usage

### Creating a new site

Run the following command

```console
cd path/to/your_site/directory
papery init
```

### Run with the development server

```console
papery run
```

You can see your web site via <http://localhost:8000>. All pages are automatically updated when you modified any resources.

### Build manually

```console
papery build
```

### Apply local Markdownlint rules

You can set local Markdownlint rule file for Markdown file validation. By setting it anywhere under `path/to/your_site/directory`, it has priority over the [default rules](https://github.com/withletters/papery/blob/master/papery/lint_configs/markdownlint.yaml).

Filenames ending with `markdownlint.yaml` or `markdownlint.yml` can be used to apply Markdownlint local rules.

## Development

```console
uv sync          # create .venv with dependencies
uv run papery    # run the CLI from the working tree
uv run pytest    # run tests
uv build         # build sdist and wheel into dist/
```

## TODO

- documentation
- styling with SASS/SCSS

## License

Copyright 2013-2023 [Xcoo, Inc.][xcoo]

Licensed under the [Apache License, Version 2.0][apache-license-2.0].

[xcoo]: https://xcoo.com
[apache-license-2.0]: http://www.apache.org/licenses/LICENSE-2.0.html

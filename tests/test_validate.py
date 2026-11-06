import os

import pytest

from papery.validate import Validator

SAMPLE_CONFIG = os.path.join(os.path.dirname(__file__), '..', 'papery', 'data', 'sample', 'config.yml')


def test_valid_config():
    Validator().validate_config(SAMPLE_CONFIG)


def test_invalid_config(tmp_path, capsys):
    config = tmp_path / 'config.yml'
    config.write_text('---\ntitle: no author\n', encoding='utf-8')

    with pytest.raises(SystemExit) as e:
        Validator().validate_config(str(config))

    assert e.value.code == 1
    assert "Cannot find required key 'author'" in capsys.readouterr().out

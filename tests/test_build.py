import yaml

from papery.papery import Papery


def test_init_and_build_sample_site(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    Papery().initialize()

    with open('config.yml', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    Papery(config).render(skip_validation=True)

    index = (tmp_path / 'output' / 'index.html').read_text(encoding='utf-8')
    assert 'Strawberries' in index
    assert (tmp_path / 'output' / 'sitemap.xml').exists()
    assert (tmp_path / 'output' / 'assets' / 'css' / 'style.css').exists()

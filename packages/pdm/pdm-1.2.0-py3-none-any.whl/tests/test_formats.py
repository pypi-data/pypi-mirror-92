from pdm.formats import flit, legacy, pipfile, poetry, requirements
from pdm.utils import cd
from tests import FIXTURES


def test_convert_pipfile(project):
    golden_file = FIXTURES / "Pipfile"
    assert pipfile.check_fingerprint(project, golden_file)
    result, settings = pipfile.convert(project, golden_file)

    assert settings["allow_prereleases"]
    assert result["requires-python"] == ">=3.6"

    assert not result["dev-dependencies"]

    assert "requests" in result["dependencies"]
    assert 'pywinusb; sys_platform == "win32"' in result["dependencies"]

    assert settings["source"][0]["url"] == "https://pypi.python.org/simple"


def test_convert_requirements_file(project):
    golden_file = FIXTURES / "requirements.txt"
    assert requirements.check_fingerprint(project, golden_file)
    result, settings = requirements.convert(project, golden_file)

    assert len(settings["source"]) == 2
    assert "webassets==2.0" in result["dependencies"]
    assert 'whoosh==2.7.4; sys_platform == "win32"' in result["dependencies"]
    assert (
        "-e git+https://github.com/pypa/pip.git@master#egg=pip"
        in result["dependencies"]
    )


def test_convert_poetry(project):
    golden_file = FIXTURES / "pyproject-poetry.toml"
    assert poetry.check_fingerprint(project, golden_file)
    with cd(FIXTURES):
        result, _ = poetry.convert(project, golden_file)

    assert result["authors"][0] == {
        "name": "Sébastien Eustace",
        "email": "sebastien@eustace.io",
    }
    assert result["name"] == "poetry"
    assert result["version"] == "1.0.0"
    assert result["license"] == {"text": "MIT"}
    assert "classifiers" in result["dynamic"]
    assert "repository" in result["urls"]
    assert result["requires-python"] == ">=2.7,<4.0,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*"
    assert 'cleo<1.0.0,>=0.7.6; python_version ~= "2.7"' in result["dependencies"]
    assert (
        'cachecontrol[filecache]<1.0.0,>=0.12.4; python_version >= "3.4" '
        'and python_version < "4.0"' in result["dependencies"]
    )
    assert "babel==2.9.0" in result["dependencies"]
    assert "mysql" in result["optional-dependencies"]
    assert "psycopg2<3.0,>=2.7" in result["optional-dependencies"]["pgsql"]
    assert len(result["dev-dependencies"]) == 2

    assert result["scripts"] == {"poetry": "poetry.console:run"}
    assert result["entry-points"]["blogtool.parsers"] == {
        ".rst": "some_module:SomeClass"
    }
    assert result["includes"] == ["lib/my_package", "tests", "CHANGELOG.md"]
    assert result["excludes"] == ["my_package/excluded.py"]


def test_convert_flit(project):
    golden_file = FIXTURES / "projects/flit-demo/pyproject.toml"
    assert flit.check_fingerprint(project, golden_file)
    result, _ = flit.convert(project, golden_file)

    assert result["name"] == "pyflit"
    assert result["version"] == "0.1.0"
    assert "classifiers" in result["dynamic"]
    assert result["authors"][0] == {
        "name": "Thomas Kluyver",
        "email": "thomas@kluyver.me.uk",
    }
    assert result["urls"]["homepage"] == "https://github.com/takluyver/flit"
    assert result["requires-python"] == ">=3.5"
    assert result["readme"] == "README.rst"
    assert result["urls"]["Documentation"] == "https://flit.readthedocs.io/en/latest/"
    assert result["dependencies"] == [
        "requests >=2.6",
        "configparser; python_version == '2.7'",
    ]

    assert result["optional-dependencies"]["test"] == [
        "pytest >=2.7.3",
        "pytest-cov",
    ]

    assert result["scripts"]["flit"] == "flit:main"
    assert (
        result["entry-points"]["pygments.lexers"]["dogelang"]
        == "dogelang.lexer:DogeLexer"
    )
    assert result["includes"] == ["doc/"]
    assert result["excludes"] == ["doc/*.html"]


def test_convert_legacy_format(project):
    golden_file = FIXTURES / "pyproject-legacy.toml"
    assert legacy.check_fingerprint(project, golden_file)
    result, settings = legacy.convert(project, golden_file)

    assert result["name"] == "demo-package"
    assert result["authors"][0] == {"name": "frostming", "email": "mianghong@gmail.com"}
    assert result["license"] == {"text": "MIT"}
    assert sorted(result["dynamic"]) == ["classifiers", "version"]
    assert result["dependencies"] == ["flask"]
    assert not result["dev-dependencies"]
    assert result["optional-dependencies"]["test"] == ["pytest"]
    assert settings["source"][0]["url"] == "https://test.pypi.org/simple"

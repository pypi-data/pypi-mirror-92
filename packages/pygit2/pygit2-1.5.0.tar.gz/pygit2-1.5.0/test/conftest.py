import os

import pytest
import pygit2
from . import utils


@pytest.fixture(scope='session', autouse=True)
def disable_global_git_config():
    """
    Do not use global config for better test reproducibility.
    https://github.com/libgit2/pygit2/issues/989
    """
    levels = [pygit2.GIT_CONFIG_LEVEL_GLOBAL,
              pygit2.GIT_CONFIG_LEVEL_XDG,
              pygit2.GIT_CONFIG_LEVEL_SYSTEM]
    for level in levels:
        pygit2.settings.search_path[level] = ""


@pytest.fixture
def pygit2_empty_key():
    path = os.path.join(os.path.dirname(__file__), 'keys', 'pygit2_empty')
    return path, f'{path}.pub', 'empty'


@pytest.fixture
def barerepo(tmp_path):
    with utils.TemporaryRepository('testrepo.git', tmp_path) as path:
        yield pygit2.Repository(path)


@pytest.fixture
def barerepo_path(tmp_path):
    with utils.TemporaryRepository('testrepo.git', tmp_path) as path:
        yield pygit2.Repository(path), path


@pytest.fixture
def dirtyrepo(tmp_path):
    with utils.TemporaryRepository('dirtyrepo.tar', tmp_path) as path:
        yield pygit2.Repository(path)


@pytest.fixture
def emptyrepo(tmp_path):
    with utils.TemporaryRepository('emptyrepo.tar', tmp_path) as path:
        yield pygit2.Repository(path)

@pytest.fixture
def encodingrepo(tmp_path):
    with utils.TemporaryRepository('encoding.tar', tmp_path) as path:
        yield pygit2.Repository(path)


@pytest.fixture
def mergerepo(tmp_path):
    with utils.TemporaryRepository('testrepoformerging.tar', tmp_path) as path:
        yield pygit2.Repository(path)


@pytest.fixture
def testrepo(tmp_path):
    with utils.TemporaryRepository('testrepo.tar', tmp_path) as path:
        yield pygit2.Repository(path)


@pytest.fixture
def testrepo_path(tmp_path):
    with utils.TemporaryRepository('testrepo.tar', tmp_path) as path:
        yield pygit2.Repository(path), path


@pytest.fixture
def testrepopacked(tmp_path):
    with utils.TemporaryRepository('testrepopacked.tar', tmp_path) as path:
        yield pygit2.Repository(path)

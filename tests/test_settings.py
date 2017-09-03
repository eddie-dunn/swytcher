"""Tests for settings.py"""
# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=protected-access
import collections
import unittest

import pytest

import swytcher.settings as settings


@pytest.fixture
def os_mock(monkeypatch):
    """Path out os"""
    mock_os = unittest.mock.MagicMock(spec=settings.os)
    mock_os.path.expanduser.return_value = '/home/foouser'
    monkeypatch.setattr(settings, 'os', mock_os)
    return mock_os


# setup_layouts
def test_setup_layouts():
    """Test setup_layouts"""
    class TestXkb:  # pylint: disable=too-few-public-methods
        groups_names = ('layout1', 'layout2')

    config = collections.OrderedDict((
        ('layout_1', {'strings': 'foo', 'substrings': 'bar'}),
        ('layout_2', {'strings': 'baz', 'substrings': 'qux'}),
    ))
    msettings = settings.setup_layouts(TestXkb(), config=config)
    expected = [
        {'name': 'layout1', 'strings': ['foo'], 'substrings': ['bar']},
        {'name': 'layout2', 'strings': ['baz'], 'substrings': ['qux']},
    ]
    assert msettings == expected


def test_setup_layouts_config_not_loaded():
    """Test assertion error when config is not available"""
    with pytest.raises(AssertionError):
        class TestXkb:  # pylint: disable=too-few-public-methods
            groups_names = ('layout1', 'layout2')
        settings.setup_layouts(TestXkb(), None)


# _setup_logging
def test_setup_logging_conf_lacks_log_setting():
    """Test behavior when loglevel cannot be retrieved from config; this may
    happen if the config lacks a logging setting, which is OK."""
    config = {'logging': {}}
    settings._setup_logging(config)


# _get_configparser
def test_get_configparser_filenotfound(monkeypatch):
    mock_parser = unittest.mock.MagicMock(spec=settings.configparser)
    mock_parser.ConfigParser().__bool__.return_value = False
    monkeypatch.setattr(settings, 'configparser', mock_parser)
    with pytest.raises(FileNotFoundError):
        settings._get_configparser()


def test_get_configparser_default_conf(monkeypatch):
    mock_parser = unittest.mock.MagicMock(spec=settings.configparser)
    mock_parser.ConfigParser().__bool__.return_value = True
    monkeypatch.setattr(settings, 'configparser', mock_parser)

    get_config_mock = unittest.mock.MagicMock(
        spec=settings.get_config, return_value=None)
    monkeypatch.setattr(settings, 'get_config', get_config_mock)

    monkeypatch.setattr(settings.shutil, 'copy', unittest.mock.MagicMock)

    assert settings._get_configparser()


# get_config
def test_get_config(os_mock):
    # pylint: disable=redefined-outer-name
    """Test that get_config returns a string"""
    os_mock.path.isfile.return_value = True
    assert '/conf.ini' in settings.get_config('conf.ini')


def test_get_config_fail(os_mock):
    # pylint: disable=redefined-outer-name
    """Test that get_config returns a string"""
    os_mock.path.isfile.return_value = False
    assert settings.get_config('conf.ini') == ''


# conf_paths
def test_conf_paths(os_mock):
    # pylint: disable=redefined-outer-name,unused-argument
    assert (settings.conf_paths('foo_file')[0] ==
            '/home/foouser/.config/swytcher/foo_file')


# default_conf_name
def test_conf_not_found(os_mock):
    # pylint: disable=redefined-outer-name,unused-argument
    default_conf = settings.default_conf_name('name')
    assert default_conf.endswith('name')


# copy_config
def test_copy_config_ok(monkeypatch):
    mock = unittest.mock.MagicMock()
    mock.copy.return_value = 'foo'
    monkeypatch.setattr(settings, 'shutil', mock)
    assert settings.copy_config('doesntexist.ini') == 'foo'


def test_copy_config_nok(monkeypatch):
    mock = unittest.mock.MagicMock()
    mock.path.isfile.return_value = True
    monkeypatch.setattr(settings, 'os', mock)
    monkeypatch.setattr(settings, 'shutil', mock)
    with pytest.raises(FileExistsError):
        settings.copy_config('doesntexist.ini')

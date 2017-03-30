"""Tests for settings.py"""
# pylint: disable=missing-docstring
import unittest

import pytest

import swytcher.settings as settings


@pytest.fixture
def os_mock(monkeypatch):
    """Path out os"""
    mock_os = unittest.mock.MagicMock(spec=settings.os)
    mock_os.path.expanduser.return_value = '/home/foouser'
    mock_os.path.isfile.return_value = 'my/file/path'
    monkeypatch.setattr(settings, 'os', mock_os)
    return mock_os


def test_setup_layouts():
    """Test setup_layouts"""
    class TestXkb:  # pylint: disable=too-few-public-methods
        groups_names = ('layout1', 'layout2')
    msettings = settings.setup_layouts(TestXkb())
    assert (
        (msettings[0]['name'], msettings[1]['name']) ==
        ('layout1', 'layout2')
    )


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

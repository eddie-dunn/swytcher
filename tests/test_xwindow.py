"""Tests for xwindow.py"""
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
from unittest.mock import MagicMock

import pytest
import Xlib

from swytcher import xwindow


# fixtures
@pytest.fixture(autouse=True)
def xlib(monkeypatch):
    """Mock out Xlib"""
    mock_xlib = MagicMock(spec=xwindow.Xlib)
    monkeypatch.setattr(xwindow, 'Xlib', mock_xlib)
    return mock_xlib


# get_window_name
def test_get_window_name():
    """when get_wm_name() works"""
    window = MagicMock(spec=Xlib.xobject.drawable.Window)
    window_name = 'my name'
    window.get_wm_name.return_value = window_name
    name = xwindow.get_window_name(window)
    assert name == window_name


def test_get_window_name_closure():
    """when get_wm_name() doesn't work"""
    window = MagicMock(spec=Xlib.xobject.drawable.Window)
    window.get_wm_name.return_value = ''

    window_name = 'my name'
    window.get_full_text_property.return_value = window_name
    name = xwindow.get_window_name(window)
    assert name == window_name


def test_get_window_name_closer():
    """when get_wm_name() doesn't work"""
    window = MagicMock(spec=Xlib.xobject.drawable.Window)
    window.get_wm_name.return_value = ''
    window.get_full_text_property.return_value = ''

    name = xwindow.get_window_name(window)
    assert not name


# handle_xevent
def test_handle_xevent_type_not_valid():
    """Return false when event type is invalid"""
    event = MagicMock(spec=Xlib.X.PropertyNotify)
    event.type = 'invalid'
    result = xwindow.handle_xevent(event, callback=lambda *args: None)
    assert result is False


def test_handle_xevent_atom_not_valid():
    """Return false when event type is invalid"""
    event = MagicMock(spec=Xlib.protocol.event.PropertyNotify)
    event.type = xwindow.Xlib.X.PropertyNotify
    event.atom = 'invalid'
    result = xwindow.handle_xevent(event, callback=lambda *args: None)
    assert result is False


def test_handle_xevent_atom_ok(monkeypatch):
    """Return false when event type is invalid"""
    event = MagicMock(spec=Xlib.protocol.event.PropertyNotify)
    event.type = xwindow.Xlib.X.PropertyNotify
    event.atom = xwindow.NET_ACTIVE_WINDOW

    monkeypatch.setattr(xwindow, 'ROOT', MagicMock())
    monkeypatch.setattr(xwindow, 'DISP', MagicMock())
    result = xwindow.handle_xevent(
        event, callback=lambda *args, **kwargs: 'callback')
    assert result is True

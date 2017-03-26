#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name
# pylint: disable=protected-access
"""
test_swytcher
----------------------------------

Tests for `swytcher` module.
"""
from unittest.mock import Mock

import pytest

from swytcher import swytcher


# Fixtures
@pytest.fixture(autouse=True)
def xkbgroup_patch(monkeypatch):
    """Patch out xkbgroup so that we don't accidentally change keyboard
    settings when running tests."""
    mock = Mock(spec=swytcher.xkbgroup)
    monkeypatch.setattr(swytcher, 'xkbgroup', mock)
    return mock


@pytest.fixture(autouse=True)
def notify_patch(monkeypatch):
    """Patch out the notify function so that we don't send notifications when
    running tests."""
    notify_mock = Mock()
    monkeypatch.setattr(swytcher, 'notify', notify_mock)
    return notify_mock


# change_layout
def test_change_layout_changed():
    """change_layout success"""
    xkb = Mock()
    xkb.group_name = 'original_layout'

    layout = 'new_layout'
    assert swytcher.change_layout(xkb, layout) is True
    assert xkb.group_name == layout


def test_change_layout_unchanged():
    """change_layout failure"""
    layout = 'current_layout'
    xkb = Mock()
    xkb.group_name = layout

    assert swytcher.change_layout(xkb, layout) is False
    assert xkb.group_name == layout


# matches
def test_matches_no_match():
    """matches should return False when nothing matches"""
    name_list = ('foo', 'spamm', 'baz')
    strings = ('spam', 'ham')
    substrings = ('eggs', 'parrot')
    result = swytcher.matches(name_list, strings, substrings)
    assert not result


def test_matches_strings():
    """should find string match"""
    name_list = ('foo', 'ham', 'baz')
    strings = ('spam', 'ham')
    substrings = ('eggs', 'parrot')
    result = swytcher.matches(name_list, strings, substrings)
    assert result == {'ham'}


def test_matches_sub_strings():
    """should find substring match"""
    name_list = ('foo', 'hamm', 'sausage eggs and bacon')
    strings = ('spam', 'ham')
    substrings = ('egg', 'parrot')
    result = swytcher.matches(name_list, strings, substrings)
    assert result == {'sausage eggs and bacon'}


# _match_substrings
def test_match_substrings_found():
    """should find substring match"""
    name_list = ('foo', 'bar', 'sausage eggs and bacon', 'baz')
    substrings = ('egg', 'parrot')
    result = swytcher._match_substrings(name_list, substrings)
    assert result == {'sausage eggs and bacon'}


def test_match_substrings_not_found():
    """should find substring match"""
    name_list = ('foo', 'bar', 'sausage and bacon', 'baz')
    substrings = ('egg', 'parrot')
    result = swytcher._match_substrings(name_list, substrings)
    assert not result

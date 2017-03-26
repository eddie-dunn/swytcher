"""Tests for settings.py"""
# pylint: disable=missing-docstring
import swytcher.settings as settings


def test_setup_layouts():
    """Test setup_layouts"""
    class TestXkb:  # pylint: disable=too-few-public-methods
        groups_names = ('layout1', 'layout2')
    msettings = settings.setup_layouts(TestXkb())
    assert (
        (msettings[0]['name'], msettings[1]['name']) ==
        ('layout1', 'layout2')
    )

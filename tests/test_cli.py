"""Tests for cli.py"""
import unittest

import pytest
from click.testing import CliRunner

from swytcher import cli


@pytest.fixture(autouse=True)
def mock_swytcher(monkeypatch):
    """Patch out swytcher module"""
    mock = unittest.mock.MagicMock()
    monkeypatch.setattr(cli, 'swytcher', mock)
    return mock


def test_command_line_interface():
    """CLI should return help text"""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'swytcher.cli' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output

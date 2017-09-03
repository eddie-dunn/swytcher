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
    assert '--help' in help_result.output


def test_cli_cpcfg(monkeypatch):
    """CLI should handle cpcfg command"""
    mock = unittest.mock.MagicMock()
    # mock.side_effect =
    monkeypatch.setattr(cli, 'settings', mock)
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--cpcfg'])
    assert help_result.exit_code == 0
    assert 'Sample config copied to' in help_result.output


def test_cli_cpcfg_fail(monkeypatch):
    """CLI should handle cpcfg command"""
    mock = unittest.mock.MagicMock()
    mock.copy_config.side_effect = FileExistsError('err')
    monkeypatch.setattr(cli, 'settings', mock)
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--cpcfg'])
    assert (help_result.exit_code == 2 and
            'Sample config NOT copied;' in help_result.output)

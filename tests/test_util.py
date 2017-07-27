"""Tests for util.py"""
# pylint: disable=missing-docstring
import logging
import unittest.mock

import swytcher.util as util


def test_suppress_err():
    """happy path testing for exception handler"""
    @util.suppress_err(KeyError)
    @util.suppress_err(TypeError)
    @util.suppress_err(IndexError)
    def testfunc():
        return 'foo'
    assert testfunc() == 'foo'


def test_suppress_err_logs():
    """test that exception was logged after being suppressed"""
    logger = unittest.mock.MagicMock(spec=logging.getLogger(__name__))

    @util.suppress_err(IndexError, logger)
    def testfunc():
        raise IndexError("wrong")

    testfunc()
    assert logger.log.called


def test_suppress_err_no_logging():
    """test that exception was logged after being suppressed"""
    @util.suppress_err(IndexError)
    def testfunc():
        raise IndexError("wrong")

    testfunc()

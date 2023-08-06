#!/usr/bin/env python

"""Tests for `bjorn` package."""
import os

os.environ["JOB_SETTINGS"] = "tests.settings"
from bjorn.config import settings

def test_content_settings():
    assert settings.VALUE_TO_TEST == "A"


def test_get_logger():
    LOGGER = settings.get_job_logger("job")
    LOGGER.info('bjorn info')
    LOGGER.warning('bjorn warning')
    LOGGER.error('bjorn error')
    LOGGER.critical('bjorn critical')
    assert True


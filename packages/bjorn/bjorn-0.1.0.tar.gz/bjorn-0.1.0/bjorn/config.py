"""
Configuration file settings
"""
import os
import importlib
import logging

from logging.config import dictConfig


class JobConfig():
    """
    class that envolve de settings configuration
    """

    def __init__(self, settings, **kwargs):
        super().__init__(**kwargs)
        ref_settings = importlib.import_module(settings)
        self.__dict__ = ref_settings.__dict__.copy()

    def init(self):
        logging.config.dictConfig(self.LOGGING_CONFIG)
        return self

    @staticmethod
    def get_job_logger(name):
        return logging.getLogger(name)


JOB_SETTINGS = os.getenv("JOB_SETTINGS", "settings")
settings = JobConfig(JOB_SETTINGS).init()

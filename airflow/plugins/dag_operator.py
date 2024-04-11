# Databricks notebook source
import os
from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class FileSensor(BaseSensorOperator):
    """
    Sensor to check for the existence of a file at a certain path.
    """

    @apply_defaults
    def __init__(self, filepath, *args, **kwargs):
        super(FileSensor, self).__init__(*args, **kwargs)
        self.filepath = filepath

    def poke(self, context):
        self.log.info(f'Checking if file {self.filepath} exists')
        return os.path.isfile(self.filepath)

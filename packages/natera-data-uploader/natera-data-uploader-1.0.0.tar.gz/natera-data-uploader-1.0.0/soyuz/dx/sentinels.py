#!/usr/bin/env python

import os
from abc import ABCMeta, abstractmethod

import dxpy

from soyuz import __version__ as version
from soyuz.dx.variables import Type, Property


class SentinelBase(object):
    __metaclass__ = ABCMeta

    DATA_KEY = "data"
    METRICS_KEY = "run_metrics"
    DX_LINK_KEY = "$dnanexus_link"

    def __init__(self, basedir, name):
        self._dxrecord = dxpy.new_dxrecord(types=[Type.UPLOAD_SENTINEL],
                                           folder=os.path.join(basedir, name).replace("\\", "/"),
                                           name="{}_upload_sentinel".format(name),
                                           properties={Property.RUN_FOLDER: name,
                                                       Property.VERSION: version},
                                           parents=True)

    @abstractmethod
    def add_file(self, data_file, file_id):
        raise NotImplementedError()

    def get_id(self):
        return self._dxrecord.get_id()

    def close(self):
        self._dxrecord.close()


class WesSignateraSentinel(SentinelBase):
    def add_file(self, data_file, file_id):
        details = self._dxrecord.get_details()
        sample_id = data_file.get_sample_id()
        if sample_id:
            self._dxrecord.add_tags([sample_id])
            self.__add_data_file_details(details, sample_id, file_id)
        else:
            self.__add_metrics_details(details, file_id)
        self._dxrecord.set_details(details)

    @staticmethod
    def __add_data_file_details(details, sample_id, file_id):
        if SentinelBase.DATA_KEY not in details:
            details[SentinelBase.DATA_KEY] = {}
        data_details = details[SentinelBase.DATA_KEY]
        if sample_id not in data_details:
            data_details[sample_id] = []
        data_details[sample_id].append({SentinelBase.DX_LINK_KEY: file_id})

    @staticmethod
    def __add_metrics_details(details, file_id):
        if SentinelBase.METRICS_KEY not in details:
            details[SentinelBase.METRICS_KEY] = []
        details[SentinelBase.METRICS_KEY].append({SentinelBase.DX_LINK_KEY: file_id})


class RawSentinel(SentinelBase):
    def add_file(self, data_file, file_id):
        pass

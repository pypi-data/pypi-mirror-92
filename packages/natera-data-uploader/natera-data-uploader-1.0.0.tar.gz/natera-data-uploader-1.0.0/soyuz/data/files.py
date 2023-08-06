#!/usr/bin/env python

import os
import re
from abc import ABCMeta, abstractmethod

from soyuz.dx.variables import Type


class DataFile(object):
    __metaclass__ = ABCMeta

    def __init__(self, location, name, seq_folder):
        self.__location = location
        self.__name = name
        self.__seq_folder = seq_folder

    def get_location(self):
        return self.__location

    def get_name(self):
        return self.__name

    @property
    def is_valid(self):
        return bool(self.get_regex().match(self.get_name()))

    def get_seq_folder_name(self):
        return self.__seq_folder.get_name()

    def get_relative_path(self):
        relpath = os.path.relpath(self.get_location(), self.__seq_folder.get_path())
        if relpath == ".":
            return ""
        return relpath

    def get_full_path(self):
        return os.path.join(self.__location, self.__name)

    @abstractmethod
    def get_type(self):
        raise NotImplementedError()

    @abstractmethod
    def get_regex(self):
        raise NotImplementedError()

    @abstractmethod
    def get_sample_id(self):
        raise NotImplementedError()


class RawDataFile(DataFile):
    def get_sample_id(self):
        return None

    def get_type(self):
        return None

    def get_regex(self):
        return re.compile(".+?")


class WesDataFile(DataFile):
    def get_regex(self):
        return re.compile("(?P<sample_id>[A-Za-z0-9-.]*)_[A-Za-z0-9-_]*.(?P<extension>fastq.gz|fastq|bam)")

    def get_type(self):
        m = self.get_regex().match(self.get_name())
        if m:
            extension = m.group("extension")
            if extension == "fastq.gz" or extension == "fastq":
                return Type.FASTQ
            if extension == "bam":
                return Type.BAM
        return None

    def get_sample_id(self):
        m = self.get_regex().match(self.get_name())
        if m:
            return m.group("sample_id")
        return None


class QcDataFile(DataFile):
    def get_regex(self):
        return re.compile("[A-Za-z0-9-_ ]*.(?P<extension>csv|pdf|xlsx)")

    def get_type(self):
        m = self.get_regex().match(self.get_name())
        if m:
            extension = m.group("extension")
            if extension == "csv":
                return Type.CSV
            if extension == "pdf":
                return Type.PDF
            if extension == "xlsx":
                return Type.XLSX
        return None

    def get_sample_id(self):
        return None

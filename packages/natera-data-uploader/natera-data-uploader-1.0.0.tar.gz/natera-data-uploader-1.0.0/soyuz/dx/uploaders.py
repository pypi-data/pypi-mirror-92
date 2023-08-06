#!/usr/bin/env python

import logging
import os
import time
import subprocess
from abc import ABCMeta, abstractmethod

import dxpy

from soyuz.dx.sentinels import WesSignateraSentinel, RawSentinel
from soyuz.dx.variables import Type, Property
from soyuz.data.folders import *
from soyuz.utils import UploaderException


class WatchUploader(object):
    __metaclass__ = ABCMeta

    def __init__(self, dx, basedir, interval):
        self._dx = dx
        self._basedir = basedir
        self.interval = interval
        self.ua_path = None

    def watch(self, watch_dir):
        while True:
            for seq_folder in watch_dir.get_seq_folders():
                try:
                    uploader = DxUploaderFactory.create(self._dx, self._basedir, seq_folder)
                    uploader.ua_path = self.ua_path
                    uploader.upload(seq_folder)
                except UploaderException as e:
                    logging.error("{}. Skipping".format(e))
                    continue
            time.sleep(self.interval)


class DxUploaderBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, dx, basedir):
        self._dx = dx
        self._basedir = basedir
        self.ua_path = None

    def upload(self, seq_folder):
        self.__validate_target_dir(seq_folder)

        logging.info("Starting upload for {}".format(seq_folder.get_name()))
        sentinel = self._create_sentinel(seq_folder.get_name())
        for data_file in seq_folder.list_files():
            remote_folder = os.path.join(self._basedir,
                                         data_file.get_seq_folder_name(),
                                         data_file.get_relative_path()).replace("\\", "/")
            types = self._get_additional_types(data_file)
            types.append(Type.UPLOAD_DATA)
            properties = self._get_additional_properties(data_file, seq_folder.get_name())
            properties[Property.RUN_FOLDER] = seq_folder.get_name()
            if self.ua_path and os.path.isfile(self.ua_path):
                dx_file = self.ua_upload_file_with_details(data_file, remote_folder, types, properties)
            else:
                dx_file = self.dx_upload_file_with_details(data_file, remote_folder, types, properties)
            sentinel.add_file(data_file, dx_file.get_id())
        sentinel.close()
        logging.info("{} has been successfully uploaded".format(seq_folder.get_name()))

    def __validate_target_dir(self, folder):
        if not folder.is_valid:
            raise UploaderException(
                    "{} is not valid".format(folder.get_name()))
        project = dxpy.DXProject(self._dx.get_project_id())
        try:
            entities = project.list_folder(os.path.join(self._basedir, folder.get_name()))
            if len(entities["objects"]) > 0 or len(entities["folders"]) > 0:
                raise UploaderException(
                    "{} already exists under {}".format(folder.get_name(), self._basedir))
        except dxpy.exceptions.ResourceNotFound:
            pass

    def ua_upload_file_with_details(self, data_file, remote_folder, types, properties):
        args = [r'"{}"'.format(self.ua_path), data_file.get_full_path().replace("(", "\(").replace(")", "\)")]
        args.extend(["--auth-token", self._dx.get_token()])
        args.extend(["-p", self._dx.get_project_id()])
        args.extend(["-f", remote_folder])
        args.extend(["-g --do-not-compress"])
        args.extend(["--type {}".format(_type) for _type in types])
        args.extend(["--property {}={}".format(key, val) for key, val in properties.items()])
        subprocess.check_output(" ".join(args), shell=True)
        objects = list(dxpy.bindings.find_data_objects(classname="file",
                                                       folder=remote_folder,
                                                       describe=True,
                                                       project=self._dx.get_project_id(),
                                                       return_handler=True))
        return objects[0] if objects else None

    def dx_upload_file_with_details(self, data_file, remote_folder, types, properties):
        dx_file = self.upload_file(data_file, remote_folder)

        if dx_file:
            dx_file.add_types(types)
            dx_file.set_properties(properties)
            dx_file.close()
        else:
            raise UploaderException("Failed to upload {}".format(data_file.get_full_path()))

        return dx_file

    def upload_file(self, data_file, remote_folder):
        logging.info("Uploading {} to {}".format(data_file.get_full_path(), remote_folder))
        return dxpy.upload_local_file(data_file.get_full_path(),
                                      folder=remote_folder,
                                      keep_open=True,
                                      parents=True)

    @abstractmethod
    def _create_sentinel(self, seq_folder_name):
        raise NotImplementedError()

    @abstractmethod
    def _get_additional_types(self, data_file):
        raise NotImplementedError()

    @abstractmethod
    def _get_additional_properties(self, data_file, seq_folder_name):
        raise NotImplementedError()


class WesSignateraDxUploader(DxUploaderBase):
    SEQ_FOLDER_TYPE = WesSignateraSeqFolder

    def _create_sentinel(self, seq_folder_name):
        return WesSignateraSentinel(self._basedir, seq_folder_name)

    def _get_additional_types(self, data_file):
        types = []
        data_type = data_file.get_type()
        if data_type:
            types.append(data_type)
            if data_type == Type.CSV and data_file.get_name().startswith("WES-QCMetrics"):
                types.append(Type.WESQCREPORT)
        return types

    def _get_additional_properties(self, data_file, seq_folder_name):
        properties = {}
        if data_file.get_sample_id():
            properties[Property.SAMPLE_REFERENCE] = "{}/{}".format(seq_folder_name, data_file.get_sample_id())
        return properties


class RawDxUploader(DxUploaderBase):
    SEQ_FOLDER_TYPE = RawSeqFolder

    def _create_sentinel(self, seq_folder_name):
        return RawSentinel(self._basedir, seq_folder_name)

    def _get_additional_types(self, data_file):
        return []

    def _get_additional_properties(self, data_file, seq_folder_name):
        return {}


class BgiDxUploader(DxUploaderBase):
    SEQ_FOLDER_TYPE = BgiSeqFolder

    def _create_sentinel(self, seq_folder_name):
        return RawSentinel(self._basedir, seq_folder_name)

    def _get_additional_types(self, data_file):
        return []

    def _get_additional_properties(self, data_file, seq_folder_name):
        return {}


class DxUploaderFactory(object):
    @staticmethod
    def create(dx, basedir, seq_folder):
        if isinstance(seq_folder, BgiDxUploader.SEQ_FOLDER_TYPE):
            return BgiDxUploader(dx, basedir)
        if isinstance(seq_folder, RawDxUploader.SEQ_FOLDER_TYPE):
            return RawDxUploader(dx, basedir)
        if isinstance(seq_folder, WesSignateraDxUploader.SEQ_FOLDER_TYPE):
            return WesSignateraDxUploader(dx, basedir)
        raise UploaderException(
                "Uploader for the folder {} was not found".format(seq_folder.get_name()))

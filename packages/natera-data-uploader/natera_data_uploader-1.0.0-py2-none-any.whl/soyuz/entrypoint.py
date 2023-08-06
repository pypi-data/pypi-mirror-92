#!/usr/bin/env python

import logging

from soyuz.configuration import Parameters
from soyuz.configuration import Settings
from soyuz.data.daemons import Daemon
from soyuz.data.folders import *
from soyuz.dx.context import DxContext
from soyuz.dx.uploaders import *
from soyuz.utils import UploaderException


def main():
    try:
        params = Parameters()
        settings = Settings()

        settings.logging.initialize()

        if params.get_action() in [Parameters.UPLOAD_ACTION, Parameters.WATCH_ACTION]:

            token = params.get_token()
            if not token:
                token = settings.get_token()
            if not token:
                raise UploaderException("Token was not specified")

            dx_context = DxContext(token)

            folder = None
            uploader = None

            if params.get_action() == Parameters.UPLOAD_ACTION:
                if params.get_upload_type() == Parameters.WES_SIGNATERA_UPLOAD:
                    uploader = WesSignateraDxUploader(dx_context, settings.get_base_dir())
                    folder = WesSignateraSeqFolder(params.get_folder())
                elif params.get_upload_type() == Parameters.BGI_UPLOAD:
                    uploader = BgiDxUploader(dx_context, settings.get_base_dir())
                    folder = BgiSeqFolder(params.get_folder())
                elif params.get_upload_type() == Parameters.RAW_UPLOAD:
                    uploader = RawDxUploader(dx_context, settings.get_base_dir())
                    folder = RawSeqFolder(params.get_folder())

                if not folder or not uploader:
                    raise UploaderException("Incorrect upload type")

                if not folder.is_valid:
                    raise UploaderException("Data folder is not in a valid state")

                uploader.ua_path = settings.get_ua_path()
                uploader.upload(folder)

            elif params.get_action() == Parameters.WATCH_ACTION:

                uploader = WatchUploader(dx_context, settings.get_base_dir(), params.get_interval())
                uploader.ua_path = settings.get_ua_path()

                if params.get_watch_type() == Parameters.START_WATCH:
                    if params.foreground():
                        uploader.watch(WatchDirectory(params.get_folder()))
                    else:
                        Daemon(uploader.watch, WatchDirectory(params.get_folder())).start()
                elif params.get_watch_type() == Parameters.STOP_WATCH:
                    Daemon().stop()
                elif params.get_watch_type() == Parameters.STATUS_WATCH:
                    Daemon().status()

        elif params.get_action() == Parameters.CONFIG_ACTION:

            if params.get_config_action() == Parameters.GET_CONFIG:
                if params.get_config_parameter_key() == "token":
                    logging.info(settings.get_token())
                elif params.get_config_parameter_key() == "basedir":
                    logging.info(settings.get_base_dir())
                elif params.get_config_parameter_key() == "interval":
                    logging.info(settings.get_interval())
                elif params.get_config_parameter_key() == "ua_path":
                    logging.info(settings.get_ua_path())

            elif params.get_config_action() == Parameters.SET_CONFIG:
                if params.get_config_parameter_key() == "token":
                    settings.set_token(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "basedir":
                    settings.set_basedir(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "interval":
                    settings.set_interval(params.get_config_parameter_value())
                elif params.get_config_parameter_key() == "ua_path":
                    settings.set_ua_path(params.get_config_parameter_value())
                else:
                    raise UploaderException("There is no parameter '{}'".format(params.get_config_parameter_key()))
                settings.dump()
                logging.info("Set {} to {}".format(params.get_config_parameter_key(), params.get_config_parameter_value()))

    except UploaderException as e:
        logging.error(e)
        quit(1)


if __name__ == "__main__":
    main()

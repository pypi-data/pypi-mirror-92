import logging
import os
from pathlib import Path

import boto3

from concurrency import CallBackThread

_LOGGER = logging.getLogger('cas.model.file')


class AwsIfcFileAccess:
    """This class is used to retrieve a file from the AWS S3. When this class goes out of scope, and is garbage
    collected, the downloaded file will automatically be removed from the temporary directory"""

    def __init__(self, file_name, auto_download=True, file_available_callback=None, file_unavailable_callback=None):
        if file_available_callback is not None and not callable(file_available_callback):
            raise TypeError('expected callable function, not {0}'.format(type(file_available_callback)))

        if file_unavailable_callback is not None and not callable(file_unavailable_callback):
            raise TypeError('expected callable function, not {0}'.format(type(file_unavailable_callback)))

        self.file_name = file_name
        self.__download_thread = None
        self.__file_available_callback = file_available_callback
        self.__file_unavailable_callback = file_unavailable_callback

        _LOGGER.debug('Initialised S3 Access for IFC File "%s"', file_name)
        if auto_download:
            self.download_file()

    def __del__(self):
        _LOGGER.debug('Removing downloaded file "%s"', self.file_name)
        if self.is_file_downloaded():
            os.remove(self.get_local_file_path())

    def is_file_downloaded(self):
        return os.path.exists(self.get_local_file_path())

    def is_downloading(self):
        return self.__download_thread is not None

    def get_local_file_path(self):
        return '{0}/{1}.ifc'.format(self.__get_temp_path(), self.file_name)

    def download_file(self):
        if not self.is_file_downloaded():
            if self.__download_thread is None:
                def download_impl():
                    bucket_name = os.getenv('IFC_AWS_BUCKET_NAME', 'acabim-staging')
                    _LOGGER.debug('Starting S3 File download')
                    boto3.client('s3').download_file(Bucket=bucket_name, Key='IFC/{0}.ifc'.format(self.file_name),
                                                     Filename=self.get_local_file_path())

                self.__download_thread = CallBackThread(download_impl, callback=self.__on_download_finished,
                                                        exception_callback=self.__on_download_exception)
                self.__download_thread.setName('cas_aws_file_dl:{0}'.format(self.file_name))
                self.__download_thread.daemon = True
                self.__download_thread.start()
                _LOGGER.debug('File download started for "%s"', self.file_name)
            else:
                _LOGGER.warning('File is already downloading')
        else:
            _LOGGER.debug('File is already downloaded')

    @staticmethod
    def __get_temp_path():
        folder_path = '{0}/.local/IfcParser'.format(str(Path.home()))
        if not os.path.exists(folder_path):
            _LOGGER.debug('Creating Path "%s"', folder_path)
            os.makedirs(folder_path)

        return folder_path

    def __on_download_finished(self):
        _LOGGER.info('File "%s" download complete', self.file_name)
        self.__download_thread = None
        if self.__file_available_callback is not None:
            self.__file_available_callback(self)

    def __on_download_exception(self, exception):
        _LOGGER.exception(exception)
        self.__download_thread = None
        if self.__file_unavailable_callback is not None:
            self.__file_unavailable_callback(exception)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    AwsIfcFileAccess('Linwood')

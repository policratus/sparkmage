"""
Image Acquisition

This module has classes for automatic image acquisition
"""
import abc
import os
import multiprocessing
from icrawler.builtin import GoogleImageCrawler

class ImageAcquisitionBase(object):
    """
    Abstract class for image acquisition
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get(self, keyword, path):
        """
        Retrieves images from Google Images and
        save it to a local path
        """
        return

class ImageAcquisition(ImageAcquisitionBase):
    """
    Implementations of image acquisition
    """
    @staticmethod
    def get(keyword, path):
        """
        Performs a Google Image search and save
        result to local file system.

        Parameters
        -----------
        keyword: str
            Keyword used to search in the Google Images
            base.

        path: str
            Path where the output files will reside.
        """
        if isinstance(keyword, str) and \
                isinstance(path, str):

            # If path not exists, create.
            if not os.path.exists(path):
                os.mkdir(path)

            cpu_count = multiprocessing.cpu_count()

            google_crawler = GoogleImageCrawler(
                parser_threads=cpu_count * 8,
                downloader_threads=cpu_count * 16,
                storage={'root_dir': path}
            )

            google_crawler.crawl(keyword=keyword)

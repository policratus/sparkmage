"""
Image visualization

This module reads back the clustered images
"""
import abc
import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plot
from hdfs import InsecureClient, HdfsError

class ImageVisualizationBase(object):
    """
    Abstract for image visualization
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def show(local_path, cluster_hdfs_path):
        """
        Show images after clustering
        """
        return

class ImageVisualization(ImageVisualizationBase):
    """
    Implementation for image visualization
    """
    @staticmethod
    def _connect(host, user):
        try:
            hdfs_client = InsecureClient(host, user=user)
            _ = hdfs_client.status('/')

            return hdfs_client
        except MissingSchema:
            raise HdfsError('Error connecting to HDFS.')

    @classmethod
    def save(cls, host, user, local_path, cluster_hdfs_path):
        """
        Show images after clustering
        """
        connection = cls._connect(host, user)

        parts = connection.parts(cluster_hdfs_path)

        contents = []

        for part in parts:
            with connection.read(cluster_hdfs_path + part) as rfile:
                contents.extend(rfile.read().splitlines())

        files = [
            value.split(',')
            for value in [
                    str(content, 'utf-8')
                    for content in contents
            ]
        ]

        images_clusters = [
            list(
                map(
                    int,
                    ffile
                )
            )
            for ffile in files
        ]

        images_on_dir = os.listdir(local_path)

        for image_cluster in images_clusters:
            index = [
                idx
                for idx, im in enumerate(
                        [
                            name.startswith(
                                str(image_cluster[0]).zfill(6)
                            )
                            for name in images_on_dir
                        ]
                )
                if im
            ][0]

            image_path = local_path + '/' + images_on_dir[index]

            image = Image.open(image_path)

            draw = ImageDraw.Draw(image)

            font = ImageFont.truetype(
                os.path.dirname(
                    os.path.realpath(
                        __file__
                    )
                ) + '/../fonts/LiberationSans-Regular.ttf',
                32
            )

            draw.text(
                (0, 0),
                'Cluster: ' + str(image_cluster[1]),
                font=font
            )

            image.save(image_path)

"""
Storage - HDFS

Stores files into Hadoop Distributed File System
"""
import abc
import os
import numpy
from PIL import Image
from requests.exceptions import MissingSchema
from hdfs import InsecureClient, HdfsError

class HDFSBase(object):
    """
    Abstract class for HDFS Storage
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def put(self, host, user, local_path, remote_path):
        """
        Reads a local file and puts it
        into a HDFS valid path
        """
        return

class HDFS(HDFSBase):
    """
    Implementations of HDFS operations
    """
    @classmethod
    def _connect(cls, host, user):
        try:
            hdfs_client = InsecureClient(host, user=user)
            _ = hdfs_client.status('/')

            return hdfs_client
        except MissingSchema:
            raise HdfsError('Error connecting to HDFS.')

    @classmethod
    def put(cls, host, user, local_path, remote_path):
        """
        Reads a local file and puts it
        into a HDFS valid path

        host: str
            Where the HDFS cluster are
        user: str
            User to connect to HDFS
        local_path: str
           A valid local filesystem path
        remote_path
            A valid HDFS filesystem path
        """
        hdfs_conn = cls._connect(host, user)

        try:
            hdfs_conn.walk(remote_path)
        except HdfsError:
            hdfs_conn.makedirs(remote_path)

        for ffile in os.listdir(local_path):
            im = numpy.array(Image.open(local_path + '/' + ffile)).flatten()
            im = ','.join(str(p) for p in im.tolist())

            hdfs_conn.write(
                remote_path + os.path.splitext(ffile)[0] + '.arr',
                data=im,
                overwrite=True
            )

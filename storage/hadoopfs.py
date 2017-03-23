"""
Storage - HDFS

Stores files into Hadoop Distributed File System
"""
import abc
import multiprocessing
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
        cpu_count = multiprocessing.cpu_count()

        hdfs_conn = cls._connect(host, user)

        try:
            hdfs_conn.walk(remote_path)
        except HdfsError:
            hdfs_conn.makedirs(remote_path)

        hdfs_conn.upload(
            remote_path,
            local_path,
            overwrite=True,
            n_thread=cpu_count * 4,
            cleanup=True
        )

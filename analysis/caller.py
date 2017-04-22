"""
Caller

Calls a distributed image analyzer
"""
import os

class Caller(object):
    """
    Caller to submit Spark jobs
    """
    @staticmethod
    def _here():
        """
        Returns current directory
        """
        return os.path.dirname(
            os.path.realpath(
                __file__
            )
        )

    @classmethod
    def analyze(cls, path, remote_path, clusters):
        """
        Submit spark jobs
        """
        os.system(
            '/opt/spark/bin/spark-submit {app} {path} {remote} {clusters}'.format(
                app=cls._here() + '/clustering.py',
                path=path,
                remote=remote_path,
                clusters=clusters
            )
        )

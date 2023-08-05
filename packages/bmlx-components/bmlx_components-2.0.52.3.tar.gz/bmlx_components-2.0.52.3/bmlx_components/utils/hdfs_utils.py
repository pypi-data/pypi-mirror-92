import os
import sys
import subprocess
import logging

HADOOP_BIN = "hadoop"
JJA_CLUSTER = "jjalhcluster"
DP_CLUSTER = "dplhcluster"
QW_CLUSTER = "qwlhcluster"


def hdfs_distcp(src, dest):
    logging.info("distcp from : {} to {}".format(src, dest))
    return subprocess.Popen(
        (HADOOP_BIN, "distcp", "-p=bcaxt", "-bandwidth=1000",
         src, dest),
        stdout=sys.stdout,
        stderr=sys.stdout,
    )

def sync_to_hk_local_hdfs(src, src_name):
    logging.info("sync sources src is {}".format(src))
    jja = hdfs_distcp(src, src.replace(src_name, JJA_CLUSTER))
    dp = hdfs_distcp(src, src.replace(src_name, DP_CLUSTER))
    qw = hdfs_distcp(src, src.replace(src_name, QW_CLUSTER))

    return all([dp.wait() == 0, qw.wait() == 0, jja.wait() == 0])

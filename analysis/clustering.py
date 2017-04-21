"""
Image Analysis

Performs analysis on the image set
"""
import sys
from pyspark import SparkConf, SparkContext
from pyspark.mllib.clustering import KMeans

if __name__ == '__main__':
    path = sys.argv[1]
    remote_path = sys.argv[2]
    clusters = int(sys.argv[3])

    spark_context = SparkContext(appName='Sparkmage')

    images = spark_context.textFile(path)

    images = images.map(
        lambda l: l.split(',')
    ).map(
        lambda i: [int(c) for c in i]
    )

    model = KMeans.train(
        images,
        clusters
    )

    result = []

    for idx, image in enumerate(images.collect()):
        result.append([idx + 1, model.predict(image)])

    result = spark_context.parallelize(result)
    result = result.map(
        lambda l: ','.join(str(i) for i in l)
    )

    result.saveAsTextFile(remote_path)

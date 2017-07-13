# 👁✨ sparkmage

**A tool for blazing fast analysis and clustering of similar images using 🐘 Hadoop and ⚡ Spark.**

![Pets Cluster](https://github.com/policratus/sparkmage/blob/master/docs/clusters.jpg)

## 🛠 Installation
Assuming that you've a Unix like OS or emulation, [git](https://git-scm.com/), [Python](https://www.python.org/) 2 or 3 and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) installed, just issue:

```
mkvirtualenv sparkmage
workon sparkmage
git clone git@github.com:policratus/sparkmage.git
cd sparkmage
pip install -r requirements/requirements.txt
```

## ⚙Usage
Sparmage needs [Hadoop](https://hadoop.apache.org/) (HDFS) (tested on 2.7) and [Spark](http://spark.apache.org/) (tested on 2.1) cluster as a distributed file system and processor.

### 🎯Acquiring images
All images are imported from [Google Images](https://images.google.com). To use a specific term and download images from this term:

```
sparkmage get [term] [directory]
```

For instance, if you wish to search for dogs, just issue `sparkmage get dogs /path/to/dogs/`

### 💽Storing images
All images are first stored on local file system and after this, it's uploaded to Hadoop HDFS. To copy images from a local directory to HDFS:

```
sparkmage put http://[host]:[port] [user] [local-dir] [hdfs-dir]
```

If you want to upload your just downloaded dog images, assuming that your HDFS endpoint is `master:50070`, user owner will be `hadoop`, and your target directory is `/images/dogs`, execute `sparkmage put http://master:50070 hadoop /path/to/dogs /images/dogs`.

### 📊Analyzing images
Now, comes the time to analyze all images and separate it in groups. Just execute:

```
sparkmage analyze hdfs://[host]:[port]/path/on/hdfs \
    hdfs://[host]:[port]/cluster/output/dir \
    [number_of_groups]
```

To analyze your just uploaded dog images and find five groups on it, execute `sparkmage analyze hdfs://master:50070/images/dogs hdfs://master:50070/clusters/dogs/clusters.out 5`.

### 👁Visualizing groups
So this is the final step: see your images and find what group it pertains. Do this:

```
sparkmage save http://[host]:[port] [user] [local-dir] http://[host]:[port]/cluster/output/dir
```

For instance, to cluster your dogs images: `sparkmage save http://master:50070 hadoop /path/to/dogs http://master:50070/clusters/dogs/clusters.out`.

The cluster that image pertains will be put inside the image itself, as a watermark.

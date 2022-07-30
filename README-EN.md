# Faiss Web Service

## Overview

This project is  forked from [plippe/faiss-web-service](https://github.com/plippe/faiss-web-service) .

Then I add three new feature: 
1. Image feature extraction
2. Build Faiss index
3. Build docker which can run Faiss.

For more detail info about Faiss and this project, you can check my [blog](https://waltyou.github.io/Faiss-In-Project-English/).

### 1. Image feature extraction

This project use SIFT of OpenCv, code location is: `src/utils/feature_detect.py` .

### 2. Build Faiss index

#### A Simple Way

Code location：`src/train_index/train_index.py`.
This type index doesn't need train.

#### Build index which need pre-train

In the real world, we may use the index which need pre-train, such as "IVFx,Flat".

About how to choose what type index you need, you can refer [here](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index).

Code location：`src/train_index/train_index_with_pre_train.py`.

#### BoW

If you think the output dimension of SIFT (default is 128) is too low, you can use the [Bag of Words](https://en.wikipedia.org/wiki/Bag-of-words_model).
Code location：`src/train_index/train_index_bow.py`。

#### Build index from Javacv output feature

Code location：`src/train_index/train_index_from_java.py`。

## Begin

### Prepare

I have install Opencv 3.2 for extract feature base on original docker image. You can go [the docker hub image](https://hub.docker.com/r/waltyou/faiss-api-service/) download base image:

```sh
docker pull waltyou/faiss-api-service:1.2.1-gpu
```

## API Using Guide

### Builde Index

Start docker container：

```bash
cd src/train_index
python train_index.py
```

### Search API

```sh
# Faiss search for ids 1, 2, and 3
curl 'localhost:5000/faiss/search' -X POST -d '{"k": 5, "ids": [1, 2, 3]}'

# Faiss search for image path
curl 'localhost:5000/faiss/search' -X POST -d '{"k": 5, "image": “/image/path/imagename”}'

# Faiss search for vector file path
curl 'localhost:5000/faiss/search' -X POST -d '{"k": 5, "vectors": “/vector/file/path”}'
```

## Run

Go into docker container , and run `bin/faiss_web_service.sh` .

### Check Status

Check if container is ok：
```sh
# Healthcheck
curl 'localhost:5000/ping'

```

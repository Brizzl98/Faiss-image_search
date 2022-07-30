# Faiss Web Service

English Readme is [here](./README-EN.md).

## 简述

本项目 forked from [plippe/faiss-web-service](https://github.com/plippe/faiss-web-service)。
添加了提取图片特征向量、构建 Faiss 索引以及构建运行docker三部分。

关于 Faiss 以及其他此项目的详细信息，可以在我的blog上找到，地址在[这里](https://waltyou.github.io/Faiss-In-Project/)。

### 1. 图片特征提取

使用opencv 的SIFT 特征提取算法，代码位置：`src/utils/feature_detect.py`

### 2. 索引构建

#### 简单的构建

代码位置为：`src/train_index/train_index.py`。
这个代码里面使用的是不需要 `train` 的索引。

#### 构建需要预训练的索引

在真实使用场景下，我们会使用一些需要预训练的索引，比如"IVFx,Flat"等，关于如何选择合适的索引，请参考[这里](https://waltyou.github.io/Faiss-Indexs/#%E6%8C%91%E4%B8%80%E4%B8%AA%E5%90%88%E9%80%82%E7%9A%84-index)。
代码位置为：`src/train_index/train_index_with_pre_train.py`。

#### 词袋模型

因为SIFT默认输出维度为128维，如果觉得太低，可以使用词袋模型（BOW）。
代码实现位置在：`src/train_index/train_index_bow.py`。

#### 基于Javacv提取出的特征构建索引

代码实现位置在：`src/train_index/train_index_from_java.py`。

## 开始

### 准备环境

直接使用docker， 由于提取图片特征向量时，需要用到Opencv，所以我在 plippe 镜像的基础上又安装了 Opencv 3.2 ，这样子就可以直接在镜像内部训练 Fiass 索引了。
可以到 [the docker hub image](https://hub.docker.com/r/waltyou/faiss-api-service/) 下载基础镜像:

```sh
docker pull waltyou/faiss-api-service:1.2.1-gpu
```

如果对本项目代码进行了更新，可以重新build docker 镜像， dockerfile 内容可以参考以下：
```
FROM waltyou/faiss-api-service:1.2.1-gpu

COPY src /opt/faiss-web-service/src
COPY bin /opt/faiss-web-service/bin

```

### 运行

进入docker container 中，运行 bin/faiss_web_service.sh 即可。

## API 使用规则

### 构建索引

启动docker 容器，进入容器中:
```bash
docker run -it --rm waltyou/faiss-api-service:1.2.1-gpu bash
```

在容器内部运行：

```bash
cd src/train_index
python train_index.py
```

### 查询API

```sh
# Faiss search for ids 1, 2, and 3
curl 'localhost:5000/faiss/search' -X POST -d '{"k": 5, "ids": [1, 2, 3]}'

# Faiss search for image path
curl 'localhost:5000/faiss/search' -X POST -d '{"k": 5, "image": “/image/path/imagename”}'

# Faiss search for vector file path
curl 'localhost:5000/faiss/search' -X POST -d '{"k": 5, "vectors": “/vector/file/path”}'
```

### 检测状态

检测镜像是否成功启动：
```sh
# Healthcheck
curl 'localhost:5000/ping'

```

# 常见问题

## 1. 如果不是以"production"作为参数运行 bin/faiss_web_service.sh 的话，会提示： Failed to load python module uwsgi 。

可以忽略这个报错，如果你觉得这个错误很烦人的话，可以注释掉 `src/faiss_index/blueprint.py` 中的第9、10行。原因可以参考这里：https://www.cnblogs.com/lazyboy/archive/2013/06/03/3115451.html 。
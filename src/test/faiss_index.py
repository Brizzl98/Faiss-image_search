import numpy as np
import sys
import torch
from torchvision import models, transforms, datasets
from PIL import Image
import faiss
import base64
import io
import heapq
from torch import nn
from torch.nn import functional as F
import matplotlib.pyplot as plt
import os
import cv2
from flask import Flask, render_template, jsonify, request
import logging
import uuid

# from utils.feature_detect import get_vectors, get_sift
# from utils.read_array_from_java import read_array

sys.path.append("..")
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'


class CreateIndex(object):

    def __init__(self):
        self.transforms_ = transforms.Compose([
            transforms.Resize(size=[224, 224], interpolation=2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
        # number of k-nearest neighbours
        self.k = 10
        # Downloading a pretrained model¶
        self.model = models.resnet50(pretrained=True)
        #self.index = faiss.IndexFlatL2(2048)
        self.index = faiss.IndexIDMap2(faiss.IndexFlatL2(2048))

    def decode_img(self, base64_img):
        bytes_image = base64.b64decode(base64_img)
        buf = io.BytesIO(bytes_image)
        image = Image.open(buf)
        return image

    def pooling_output(self, x):
        for layer_name, layer in self.model._modules.items():
            x = layer(x)
            if layer_name == 'avgpool':
                break
        return x

    def image_to_tensor(self, image):
        image_tensor = self.transforms_(image)
        image_tensor = image_tensor.view(1, *image_tensor.shape)
        with torch.no_grad():
            descriptors = self.pooling_output(image_tensor.to(DEVICE)).cpu().view(1, -1).numpy()
        return image_tensor, descriptors

    def add_element(self, descriptors, id):
        id = np.array([id])
        descriptors = np.vstack(descriptors)
        self.index.add_with_ids(descriptors, id)
        self.save_index()
        return self.index, id

    # def delete_from_index(self, image_tensor):
    #     with torch.no_grad():
    #         query_tensor = self.pooling_output(image_tensor.to(DEVICE)).cpu().numpy()
    #         distances, indices = self.index.search(query_tensor.reshape(1, 2048), 1)
    #         if distances == 1:
    #             self.index.remove_ids(query_tensor)

    def l2_normalize(self, distances):
        for distance in distances:
            norm = np.sqrt(np.sum(np.square(distance)))
        return distance / norm

    def search_by_tensor(self, image_tensor, k):
        with torch.no_grad():
            query_descriptors = self.pooling_output(image_tensor.to(DEVICE)).cpu().numpy()
            distances, indices = self.index.search(query_descriptors.reshape(1, 2048), k)
        return distances, indices

    def add_to_index(self, base64_img, id):
        image = self.decode_img(base64_img)
        image_tensor, descriptors = self.image_to_tensor(image)
        #self.index = self.add_element(descriptors, id)
        self.add_element(descriptors, id)
        test = faiss.vector_to_array(self.index.id_map)
        return self.index, str(test)

    def search(self, base64_img, k):
        query_image = self.decode_img(base64_img)
        image_tensor, descriptors = self.image_to_tensor(query_image)
        distances, indices = self.search_by_tensor(image_tensor, k)
        return distances, indices

    def save_index(self):
        faiss.write_index(self.index, "vector.index")  # save the index to disk
        return self.index

    def delete_from_index(self, img_id):
        img_id = np.array([img_id])
        self.index.remove_ids(img_id)
        return "success"


    # def reconstruct_index(self, indices):
    #     images = []
    #     self.index.make_direct_map()
    #     for i in indices:
    #         images.append(self.index.reconstruct(i))
    #     return images

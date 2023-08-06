#!/usr/bin/env python
# ******************************************************************************
# Copyright 2020 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
DS-CNN model definition for CIFAR10 classification.
"""

from tensorflow.keras.layers import Input
from tensorflow.keras import Model
from tensorflow.keras.utils import get_file

# CNN2SNN imports
from cnn2snn import load_quantized_model, quantize

from ..layer_blocks import conv_block, separable_conv_block

BASE_WEIGHT_PATH = 'http://data.brainchip.com/models/ds_cnn/'


def ds_cnn_cifar10(input_shape=(32, 32, 3),
                   classes=10,
                   weight_quantization=0,
                   activ_quantization=0,
                   input_weight_quantization=None):
    """Instantiates a MobileNet-like model for the "Cifar-10" example.
    This model is based on the MobileNet architecture, mainly with fewer layers.
    The weights and activations are quantized such that it can be converted into
    an Akida model.

    This architecture is originated from https://arxiv.org/abs/1704.04861 and
    inspired from https://arxiv.org/pdf/1711.07128.pdf.

    Args:
        input_shape (tuple): input shape tuple of the model
        classes (int): number of classes to classify images into
        weight_quantization (int): sets all weights in the model to have
            a particular quantization bitwidth except for the weights in the
            first layer.

            * '0' implements floating point 32-bit weights
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        activ_quantization (int): sets all activations in the model to have a.
            particular activation quantization bitwidth.

            * '0' implements floating point 32-bit activations.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        input_weight_quantization (int): sets weight quantization in the first
            layer. Defaults to weight_quantization value.

            * 'None' implements the same bitwidth as the other weights.
            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.

    Returns:
        tf.keras.Model: a quantized Keras model for DS-CNN/cifar10
    """

    # Overrides input weight quantization if None
    if input_weight_quantization is None:
        input_weight_quantization = weight_quantization

    img_input = Input(shape=input_shape)

    x = conv_block(img_input,
                   filters=128,
                   name='conv_0',
                   kernel_size=(3, 3),
                   padding='same',
                   use_bias=False,
                   add_batchnorm=True,
                   add_activation=True)

    x = separable_conv_block(x,
                             filters=128,
                             kernel_size=(3, 3),
                             name='separable_1',
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True)

    x = separable_conv_block(x,
                             filters=256,
                             kernel_size=(3, 3),
                             name='separable_2',
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True)

    x = separable_conv_block(x,
                             filters=256,
                             kernel_size=(3, 3),
                             name='separable_3',
                             padding='same',
                             use_bias=False,
                             pooling='max',
                             add_batchnorm=True,
                             add_activation=True)

    x = separable_conv_block(x,
                             filters=512,
                             kernel_size=(3, 3),
                             name='separable_4',
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True)

    x = separable_conv_block(x,
                             filters=512,
                             kernel_size=(3, 3),
                             name='separable_5',
                             padding='same',
                             use_bias=False,
                             pooling='max',
                             add_batchnorm=True,
                             add_activation=True)

    x = separable_conv_block(x,
                             filters=512,
                             kernel_size=(3, 3),
                             name='separable_6',
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True)

    x = separable_conv_block(x,
                             filters=512,
                             kernel_size=(3, 3),
                             name='separable_7',
                             padding='same',
                             use_bias=False,
                             pooling='max',
                             add_batchnorm=True,
                             add_activation=True)

    x = separable_conv_block(x,
                             filters=1024,
                             kernel_size=(3, 3),
                             name='separable_8',
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True)

    x = separable_conv_block(x,
                             filters=1024,
                             kernel_size=(3, 3),
                             name='separable_9',
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True)

    x = separable_conv_block(x,
                             filters=classes,
                             kernel_size=(3, 3),
                             name='separable_10',
                             padding='same',
                             use_bias=False,
                             pooling='global_avg',
                             add_batchnorm=False,
                             add_activation=False)

    model = Model(img_input, x, name='ds_cnn_cifar10')

    if ((weight_quantization != 0) or (activ_quantization != 0) or
        (input_weight_quantization != 0)):
        return quantize(model, weight_quantization, activ_quantization,
                        input_weight_quantization)
    return model


def ds_cnn_cifar10_pretrained():
    """
    Helper method to retrieve a `ds_cnn_cifar10` model that was trained on
    CIFAR10 dataset.

    Returns:
        tf.keras.Model: a Keras Model instance.

    """
    model_name = 'ds_cnn_cifar10_iq4_wq4_aq4.h5'
    file_hash = '01bea3a6fc2b9d088108ed4932572efb24254016a90fc58c3b85a0de68f868d4'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)

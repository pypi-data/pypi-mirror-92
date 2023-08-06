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
DS-CNN model definition for KWS classification.
"""

from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Reshape, Activation, Flatten
from tensorflow.keras.utils import get_file

# CNN2SNN imports
from cnn2snn import load_quantized_model, quantize, quantize_layer

from ..layer_blocks import conv_block, separable_conv_block, dense_block

BASE_WEIGHT_PATH = 'http://data.brainchip.com/models/ds_cnn/'


def ds_cnn_kws(input_shape=(49, 10, 1),
               classes=33,
               include_top=True,
               weight_quantization=0,
               activ_quantization=0,
               input_weight_quantization=None,
               last_layer_activ_quantization=None):
    """Instantiates a MobileNet-like model for the "Keyword Spotting" example.

    This model is based on the MobileNet architecture, mainly with fewer layers.
    The weights and activations are quantized such that it can be converted into
    an Akida model.

    This architecture is originated from https://arxiv.org/pdf/1711.07128.pdf
    and was created for the "Keyword Spotting" (KWS) or "Speech Commands"
    dataset.

    Args:
        input_shape (tuple): input shape tuple of the model
        classes (int): optional number of classes to classify words into, only
            be specified if `include_top` is True.
        include_top (bool): whether to include the fully-connected
            layer at the top of the model.
        weight_quantization (int): sets all weights in the model to have
            a particular quantization bitwidth except for the weights in the
            first layer.

            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        activ_quantization (int): sets all activations in the model to have a
            particular activation quantization bitwidth.

            * '0' implements floating point 32-bit activations.
            * '1' through '8' implements n-bit weights where n is from 2-8 bits.
        input_weight_quantization (int): sets weight quantization in the first
            layer. Defaults to weight_quantization value.

            * 'None' implements the same bitwidth as the other weights.
            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        last_layer_activ_quantization (int): sets activation quantization in the
            layer before the last. Defaults to activ_quantization value.

            * 'None' implements the same bitwidth as the other activations.
            * '0' implements floating point 32-bit activations.
            * '1' through '8' implements n-bit weights where n is from 2-8 bits.

    Returns
        tf.keras.Model: a quantized Keras model for MobileNet/KWS
    """
    # Overrides input weight quantization if None
    if input_weight_quantization is None:
        input_weight_quantization = weight_quantization
    if last_layer_activ_quantization is None:
        last_layer_activ_quantization = activ_quantization

    if include_top and not classes:
        raise ValueError("If 'include_top' is True, 'classes' must be set.")

    img_input = Input(shape=input_shape)

    x = conv_block(img_input,
                   filters=32,
                   kernel_size=(5, 5),
                   padding='same',
                   strides=(2, 2),
                   use_bias=False,
                   name='conv_0',
                   add_batchnorm=True)

    x = separable_conv_block(x,
                             filters=64,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             name='separable_1',
                             add_batchnorm=True)

    x = separable_conv_block(x,
                             filters=64,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             name='separable_2',
                             add_batchnorm=True)

    x = separable_conv_block(x,
                             filters=64,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             name='separable_3',
                             add_batchnorm=True)

    x = separable_conv_block(x,
                             filters=64,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             name='separable_4',
                             add_batchnorm=True)

    x = separable_conv_block(x,
                             filters=64,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             name='separable_5',
                             pooling='global_avg',
                             add_batchnorm=True)

    shape = (1, 1, int(64))
    x = Reshape(shape, name='reshape_1')(x)

    x = separable_conv_block(x,
                             filters=256,
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             name='separable_6',
                             add_batchnorm=True)

    if include_top:
        x = Flatten()(x)
        x = dense_block(x,
                        units=classes,
                        name='dense_7',
                        use_bias=True,
                        add_activation=False)
        act_function = 'softmax' if classes > 1 else 'sigmoid'
        x = Activation(act_function, name=f'act_{act_function}')(x)

    model = Model(img_input, x, name='ds_cnn_kws')

    if ((weight_quantization != 0) or (activ_quantization != 0) or
        (input_weight_quantization != 0)):
        # Converts a standard sequential Keras model to a CNN2SNN Keras
        # quantized model, compatible for Akida conversion.
        model = quantize(model=model,
                         weight_quantization=weight_quantization,
                         activ_quantization=activ_quantization,
                         input_weight_quantization=input_weight_quantization)

    # Change the last layer activation bitwidth
    if last_layer_activ_quantization != activ_quantization:
        model = quantize_layer(model, 'separable_6_relu',
                               last_layer_activ_quantization)

    return model


def ds_cnn_kws_pretrained():
    """
    Helper method to retrieve a `ds_cnn_kws` model that was trained on
    KWS dataset.

    Returns:
        tf.keras.Model: a Keras Model instance.

    """
    model_name = 'ds_cnn_kws_iq8_wq4_aq4_laq1.h5'
    file_hash = 'a26240d2e284b7ecd2634f8cd77366c0a4c7bd4f39e4bde4aa7d14d5d860e09e'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)

# LeNet5 Implementation FROM SCRATCH
This is an implementation of LeNet5 from [Yann LeCun's paper](http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf) in 1998, using Numpy & OOP only (without any auto-differentiate tools or deep learning frameworks).

Yann LeCun's demo in 1993: 
<p align="center">
<a href="http://www.youtube.com/watch?feature=player_embedded&v=FwFduRA_L6Q
" target="_blank"><img src="http://img.youtube.com/vi/FwFduRA_L6Q/0.jpg" 
alt="LeNet demo" width="450" height="340" border="10" /></a></p>

## Result of Training 

Highest accuracy of 98.6% on MNIST testing dataset has achieved in 20 epoches of training (93.5% after 1st epoch). The training (20 epoches, batch size = 256) takes about 2 hours using CPU only (3.5 hours if evaluate after each epoch).

<p align="center"> 
  <img width="460" height="300" src="./Lenet5 images/errRate.png">
</p>



## File Structure

```
├── net.ipynb                          # Gradient calculations and weight updating
├── layers.ipynb                       # layers implementation for dense network
├── evaluation_matrix.ipynb            # evaluation metrics
├── Activations.ipynb                  # Activation functions
├── Utils.ipynb                        # To Load and Zero-padding
├── functional.ipynb                   # Backend for activations 
├── losses.ipynb                       # losses calculation
├── dense.ipynb                        # training and testing dense network
├── LeNet5_train.ipynb                 # Notebook for training and shows the results
├── RBF_initial_weight.ipynb           # Notebook shows the fixed weight (ASCII bitmap) in the RBF layer
├── ExeSpeedTest.ipynb                 # Comparison of different version of Conv. & Pooling functions
├── Best_model.pkl                     # The model with 98.6% accuracy both on training and testing data 
│                                      # Please download at [https://tinyurl.com/y9d7fzs9] or train one by yourself :)
│
├── MNIST_auto_Download.py             # Python script for auto-download MNIST dataset (like folder below)
├── MNIST/                             # Folder contains MNIST training and testing data
│   ├── train-images-idx3-ubyte        # Training images
│   ├── train-labels-idx1-ubyte        # Training labels
│   ├── t10k-images-idx3-ubyte         # Testing images
│   └── t10k-labels-idx1-ubyte         # Testing labels
│
└── utils/                             # Package
    ├── __init__.py 
    ├── Convolution_util.py            # Convolution forward and backward
    ├── Pooling_util.py                # Pooling forward and backward
    ├── Activation_util.py             # Activation functions
    ├── utils_func.py                  # Other functions like normalize(), initialize(), zero_pad(), etc
    ├── RBF_initial_weight.py          # Setting fixed weight (ASCII bitmap) in the RBF layer
    └── LayerObjects.py                # All the layer objects
```

## Structure of LeNet5

The structure in the original paper is:

<p align="center">
  <img width="800" src="./image/lenet5.png">
</p>

The structure used in this repo have a few modification:

1. **momentum optimizer** (momentum=0.9) is used to accelerate the training process (for faster convergence).




# Neural-Networks framework

## Contents 

* Project's main topics 
  * A [simple example CNN](#A)
  * The [Net](#The) object
* [Layers](#Layers) 
  * [Linear](#Linear)
  * [Conv2D](#Conv2D)
  * [subsampling](#subsampling)
     *[average_pool](#average pool)
  * [fcLayer](#fcLayer)
  * [RBFLayer](#RBFLayer)
* [Losses](#Losses)
  * [CrossEntropyLoss](#CrossEntropyLoss)
  * [MeanSquareLoss](#MeanSquareLoss)
* [Activations](#Activations)
  * ReLU
  * Leaky ReLU
  * Sigmoid
  * Tanh
  * squash function
  * elu
# Project's main topics 
## A simple example of NN

Its required argument is

* --dataset: path to the dataset,
while the optional arguments are

* --epochs: number of epochs,
* --batch_size: size of the training batch,
* --lr: learning rate.


## The Net object

If you would like to train the model with data X and label y, you should perform the forward pass, during which local gradients are calculated,
calculate the loss,perform the backward pass, where global gradients with respect to the variables and layer parameters are calculated,
update the weights.

In code, this looks like the following:
* ` out = net(X) `
* `loss = net.loss(out, y) `
* `net.backward()`
* `net.update_weights(lr)`

# Layers

## Linear (Fully connected layer)

A simple fully connected layer. 

Parameters:

* `in_dim`: integer, dimensions of the input.
* `out_dim`: integer, dimensions of the output.

Usage:
* input: ` numpy.ndarray  ` of shape `(N, in_dim)`.
* output: `numpy.ndarray` of shape `(N, out_dim)`.

## ConvLayer

2D convolutional layer. Parameters:
* ` in_channels `: integer, number of channels in the input image.
* ` out_channels `: integer, number of filters to be learned.
* ` kernel_size `: integer or tuple, the size of the filter to be learned. Defaults to 3.
* `  stride`: integer, stride of the convolution. Defaults to 1.
* `padding `: integer, number of zeros to be added to each edge of the images. Defaults to 0.


## Subsampling

Parameters:

2D Subsampling layer. Parameters:
* ` in_channels `: integer, number of channels in the input image.
* ` out_channels `: integer, number of filters to be learned.
* ` kernel_size `: integer or tuple, the size of the filter to be learned. Defaults to 3.
* `  stride`: integer, stride of the convolution. Defaults to 1.
* `padding `: integer, number of zeros to be added to each edge of the images. Defaults to 0.



## RBF layer
Parameters: ` weight `

# Losses

## CrossEntropyLoss

Cross-entropy loss. Usage:

*  input: ` numpy.ndarray` of shape `(N, D)` containing the class scores for each element in the batch.
*  output : float.


## MeanSquareLoss

Mean square loss. Usage:

* input : `numpy.ndarray ` of shape `(N, D)`.
* output : `numpy.ndarray` of shape `(N, D)`.

# Activations
The activation layers for the network can be found in nn.activations. They are functions, applying the specified activation function elementwisely on a numpy.ndarray. 
Currently, the following activation functions are implemented:

  * ReLU
  * Leaky ReLU
  * Sigmoid
  * Tanh
  * squash function
  * elu





## Reference

    1. [Yann LeCun's paper](http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf)
2. [Marcel Wang's blog](http://hemingwang.blogspot.tw/search/label/_社團：技術：mAiLab)
3. [Deep Learning Specialization by Andrew Ng](https://www.coursera.org/specializations/deep-learning)




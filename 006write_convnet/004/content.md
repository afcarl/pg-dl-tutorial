# VGG16

Next, let’s write some larger models in Chainer. When you write a large network consisting of several building block networks, [ChainList](https://docs.chainer.org/en/latest/reference/core/generated/chainer.ChainList.html#chainer.ChainList) is useful. First, let’s see how to write a VGG16 [[Simonyan14]](#Simonyan14) model.

---

That’s it. VGG16 is a model which won the 1st place in [classification + localization task at ILSVRC 2014](http://www.image-net.org/challenges/LSVRC/2014/results#clsloc), and since then, has become one of the standard models for many different tasks as a pre-trained model. This has 16-layers, so it’s called “VGG-16”, but we can write this model without writing all layers independently. Since this model consists of several building blocks that have the same architecture, we can build the whole network by re-using the building block definition. Each part of the network is consisted of 2 or 3 convolutional layers and activation function ([relu()](https://docs.chainer.org/en/latest/reference/generated/chainer.functions.relu.html#chainer.functions.relu)) following them, and [max_pooling_2d()](https://docs.chainer.org/en/latest/reference/generated/chainer.functions.max_pooling_2d.html#chainer.functions.max_pooling_2d) operations. This block is written as VGGBlock in the above example code. And the whole network just calls this block one by one in sequential manner.
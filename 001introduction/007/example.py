import numpy as np
import chainer
from chainer import links as L
from chainer import functions as F
from chainer import Variable


class MLP(chainer.Chain):  # MultiLayer Perceptron

    def __init__(self, n_units, n_out):
        super(MLP, self).__init__(
            # the size of the inputs to each layer will be inferred
            l1=L.Linear(None, n_units),  # n_in -> n_units
            l2=L.Linear(None, n_units),  # n_units -> n_units
            l3=L.Linear(None, n_out),  # n_units -> n_out
        )

    def __call__(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        return self.l3(h2)


model = MLP(5, 2)

x = Variable(np.ones((3, 5), dtype=np.float32))
y = model(x)

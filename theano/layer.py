import numpy as np 
import theano.tensor as T 
import theano

class Layer(object):
    """docstring for Layer"""
    def __init__(self, inputs, in_size, out_size,activation_function=None):
        super(Layer, self).__init__()
        self.W = theano.shared(np.random.normal(0, 1, (in_size, out_size)))
        self.b = theano.shared(np.zeros((out_size, )) + 0.1)
        self.Wx_plus_b = T.dot(inputs, self.w) + self.b
        self.activation_function = activation_function
        if self.activation_function is None:
            self.outputs = self.Wx_plus_b
        else:
            self.outputs = activation_function(self.Wx_plus_b)


"""[summary]
l1 = Layer(inputs, in_size=1, out_size=10, activation_function)
l2 = Layer(l1.outputs, 10, 1, None)
[description]
""" 

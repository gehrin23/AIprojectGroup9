
```python
#!/usr/bin/python
"""
A Framework of Back Propagation Neural Network (BP) model
Author: Stephen Lee
Github : https://github.com/RiptideBo
Date: 2017.11.23
"""

import numpy as np
from matplotlib import pyplot as plt


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


class DenseLayer:
    """
    Layers of BP neural network
    """

    def __init__(self, units, activation=None, learning_rate=None, is_input_layer=False):
        """
        common connected layer of bp network
        :param units: numbers of neural units
        :param activation: activation function
        :param learning_rate: learning rate for paras
        :param is_input_layer: whether it is input layer or not
        """
        self.units = units
        self.weight = None
        self.bias = None
        self.activation = activation
        if learning_rate is None:
            learning_rate = 0.3
        self.learn_rate = learning_rate
        self.is_input_layer = is_input_layer

    def initializer(self, back_units):
        rng = np.random.default_rng()
        self.weight = np.asmatrix(rng.normal(0, 0.5, (self.units, back_units)))
        self.bias = np.asmatrix(rng.normal(0, 0.5, self.units)).T
        if self.activation is None:
            self.activation = sigmoid

    def cal_gradient(self):
        # activation function may be sigmoid or linear
        if self.activation == sigmoid:
            gradient_mat = np.dot(self.output, (1 - self.output).T)
            gradient_activation = np.diag(np.diag(gradient_mat))
        else:
            gradient_activation = 1
        return gradient_activation

    def forward_propagation(self, xdata):
        self.xdata = xdata
        if self.is_input_layer:
            # input layer
            self.wx_plus_b = xdata
            self.output = xdata
            return xdata
        else:
            self.wx_plus_b = np.dot(self.weight, self.xdata) - self.bias
            self.output = self.activation(self.wx_plus_b)
            return self.output

    def back_propagation(self, gradient):
        gradient_activation = self.cal_gradient()  # i * i 维
        gradient = np.asmatrix(np.dot(gradient.T, gradient_activation))

        self._gradient_weight = np.asmatrix(self.xdata)
        self._gradient_bias = -1
        self._gradient_x = self.weight

        self.gradient_weight = np.dot(gradient.T, self._gradient_weight.T)
        self.gradient_bias = gradient * self._gradient_bias
        self.gradient = np.dot(gradient, self._gradient_x).T
        # upgrade: the Negative gradient direction
        self.weight = self.weight - self.learn_rate * self.gradient_weight
        self.bias = self.bias - self.learn_rate * self.gradient_bias.T
        # updates the weights and bias according to learning rate (0.3 if undefined)
        return self.gradient


class BPNN:
    """
    Back Propagation Neural Network model
    """

    def __init__(self):
        self.layers = []
        self.train_mse = []
        self.fig_loss = plt.figure()
        self.ax_loss = self.fig_loss.add_subplot(1, 1, 1)

    def add_layer(self, layer):
        self.layers.append(layer)

    def build(self):
        for i, layer in enumerate(self.layers[:]):
            if i < 1:
                layer.is_input_layer = True
            else:
                layer.initializer(self.layers[i - 1].units)

    def summary(self):
        for i, layer in enumerate(self.layers[:]):
            print(f"------- layer {i} -------")
            print("weight.shape ", np.shape(layer.weight))
            print("bias.shape ", np.shape(layer.bias))

    def train(self, xdata, ydata, train_round, accuracy):
        """
        train the network
        :param xdata: input data with shape (n, m)
        :param ydata: output data with shape (n, 1)
        :param train_round: round of training
        :param accuracy: acceptable loss
        """
        self.train_round = train_round
        self.accuracy = accuracy

        self.ax_loss.hlines(self.accuracy, 0, self.train_round * 1.1)

        x_shape = np.shape(xdata)
        for _ in range(train_round):
            all_loss = 0
            for row in range(x_shape[0]):
                _xdata = np.asmatrix(xdata[row, :]).T
                _ydata = np.asmatrix(ydata[row, :]).T

                # forward propagation
                for layer in self.layers:
                    _xdata = layer.forward_propagation(_xdata)

                loss, gradient = self.cal_loss(_ydata, _xdata)
                all_loss = all_loss + loss

                # back propagation: the input_layer does not upgrade
                for layer in self.layers[:0:-1]:
                    gradient = layer.back_propagation(gradient)

            mse = all_loss / x_shape[0]
            self.train_mse.append(mse)

            self.plot_loss()

            if mse < self.accuracy:
                print("----达到精度----")
                return mse
        return None

    def cal_loss(self, ydata, ydata_):
        """
        calculate loss and gradient according to output data and network output
        :param ydata: true output data with shape (n, 1)
        :param ydata_: network output data with shape (n, 1)
        :return: loss and its gradient with respect to the input layer
        """
        self.loss = np.sum(np.power((ydata - ydata_), 2))
        self.loss_gradient = 2 * (ydata_ - ydata)
        # vector (shape is the same as _ydata.shape)
        return self.loss, self.loss_gradient

    def plot_loss(self):
        """
        show loss in graph
        :return: None
        """
        if self.ax_loss.lines:
            self.ax_loss.lines.remove(self.ax_loss.lines[0])
        self.ax_loss.plot(self.train_mse, "r-")
        plt.ion()
        plt.xlabel("step")
        plt.ylabel("loss")
        plt.show()
        plt.pause(0.1)


def example():
    rng = np.random.default_rng()
    x = rng.normal(size=(10, 10))
    y = np.asarray(
        [
            [0.8, 0.4],
            [0.4, 0.3],
            [0.34, 0.45],
            [0.67, 0.32],
            [0.88, 0.67],
            [0.78, 0.77],
            [0.55, 0.66],
            [0.55, 0.4],
            [0.9, 0.2],
        ]
    )
    # create a network with one input layer and two hidden layers
    # and one output layer
    net = BPNN()
    net.add_layer(DenseLayer(10))  # first layer has 10 units
    net.add_layer(DenseLayer(10))  # second layer also has 10 units
    net.add_layer(DenseLayer(1))  # output layer has one unit

    # train the network
    mse = net.train(x, y, epoch=500, accuracy=0.02)

    print(f"final MSE: {mse}")
```

1. This code is a simple neural network implemented using NumPy. It consists of one or more layers, each of which performs a specific operation on the input data. The code first defines the `sigmoid` activation function and the `DenseLayer` class that represents a single layer in the neural network.
2. The main method `example` creates an instance of the `BPNN` class, adds one or more layers to it, trains the network on some input data, and then prints out the final mean squared error (MSE) value.
3. The `train` method takes the input data, output data, number of training rounds, and acceptable accuracy as inputs. It performs the training process by iterating over the training rounds and calculating the loss and gradient for each round. If the MSE value is smaller than the acceptable accuracy, it returns early.
4. The `cal_loss` method calculates the loss value between the true output data and the network's output data. It also calculates the gradient of the loss with respect to the input layer.
5. The `plot_loss` method plots the MSE values over time, showing the training progress.
6. Notes:
* This code is a simple example that can be used as a starting point for more complex neural network tasks.
* The accuracy parameter of the train method is set to 0.02, which means that if the MSE value is smaller than 0.02, the training process will early return and stop.
* The input data and output data are randomly generated in this example, but they can be replaced with your own data.
* You can also add more layers to the network by calling `add_layer` method multiple times.
* This code uses the default learning rate of 0.3 for all layers, you can change it by passing a different value to the `initializer` method in the layer constructor.
7. Inline comments:
* The first line of the code is the hashbang and shebang (`#!usr/bin/env python3`) which specifies the version of Python that the code should be run with.
* The next line defines the `sigmoid` activation function used in the network, it takes a single argument `x`, which can be any numpy array. It returns the value of `1/(1+np.exp(-x))`.
* The following lines define the `DenseLayer` class which represents a single layer in the neural network. It has several instance variables: `self.units`, `self.weight`, `self.bias`, and `self.activation`. The `self.weight` and `self.bias` are initialized randomly, while the `self.activation` is set to the sigmoid function by default.
* The `__init__` method of the `BPNN` class takes no arguments, it initializes an empty list for the layers.
* The `add_layer` method adds a new layer to the network by appending it to the list of layers. It also sets the `self.loss_gradient` attribute to None to indicate that the gradient should be calculated later.
* The `build` method iterates over all the layers in the network and initializes their weights and biases using the `initializer` method.
* The `summary` method simply prints out the number of units in each layer, it can be useful for debugging purposes.
* The `train` method takes the input data, output data, number of training rounds, and acceptable accuracy as inputs. It performs the training process by iterating over the training rounds and calculating the loss and gradient for each round. If the MSE value is smaller than the acceptable accuracy, it returns early.
* The `cal_loss` method calculates the loss value between the true output data and the network's output data. It also calculates the gradient of the loss with respect to the input layer.
* The `plot_loss` method plots the MSE values over time, showing the training progress.
8. Function/method documentation:
```python
#!/usr/bin/env python3
"""
A Framework of Back Propagation Neural Network (BP) model
Author: Stephen Lee
Github : https://github.com/RiptideBo
Date: 2017.11.23
"""

import numpy as np
from matplotlib import pyplot as plt


def sigmoid(x: np.ndarray) -> np.ndarray:
    """
    sigmoid activation function used in the network
    :param x: input value
    :return: output value
    """
    return 1 / (1 + np.exp(-x))


class DenseLayer:
    """
    Layers of BP neural network
    """

    def __init__(self, units, activation=None, learning_rate=None):
        """
        common connected layer of bp network
        :param units: numbers of neural units
        :param activation: activation function
        :param learning_rate: learning rate for paras
        """
        self.units = units
        self.weight = None
        self.bias = None
        self.activation = activation
        if learning_rate is None:
            learning_rate = 0.3
        self.learn_rate = learning_rate

    def initializer(self, back_units):
        """
        initialize the weights and bias of the layer
        :param back_units: number of units in previous layer
        :return: None
        """
        rng = np.random.default_rng()
        self.weight = rng.normal(0, 0.5, size=(back_units, self.units))
        self.bias = rng.normal(0, 0.5, size=self.units)
        if self.activation is None:
            self.activation = sigmoid

    def forward_propagation(self, input):
        """
        forward propagation of the layer
        :param input: input data with shape (n, m)
        :return: output data with shape (n, 1)
        """
        self.xdata = input
        if self.is_input_layer:
            # input layer
            self.wx_plus_b = self.xdata
            self.output = self.xdata
            return self.xdata
        else:
            # hidden or output layer
            self.wx_plus_b = np.dot(self.weight, self.xdata) + self.bias
            self.output = self.activation(self.wx_plus_b)
            return self.output

    def backward_propagation(self, gradient):
        """
        backward propagation of the layer
        :param gradient: gradient of the loss with respect to output layer
        :return: None
        """
        gradient_activation = self.cal_gradient()  # i * i 维
        gradient = np.dot(gradient, gradient_activation)

        self._gradient_weight = self.xdata
        self._gradient_bias = -1
        self._gradient_x = self.weight

        self.gradient_weight = np.dot(gradient.T, self._gradient_weight.T)
        self.gradient_bias = gradient * self._gradient_bias
        self.gradient = np.dot(gradient, self._gradient_x).T
        # upgrade: the Negative gradient direction
        self.weight = self.weight - self.learn_rate * self.gradient_weight
        self.bias = self.bias - self.learn_rate * self.gradient_bias
        # updates the weights and bias according to learning rate (0.3 if undefined)

    def cal_gradient(self):
        """
        calculate gradient of the loss with respect to input layer
        :return: gradient with shape (n, 1)
        """
        # activation function may be sigmoid or linear
        if self.activation == sigmoid:
            gradient_mat = np.dot(self.output, (1 - self.output).T)
            gradient_activation = np.diag(np.diag(gradient_mat))
        else:
            gradient_activation = np.identity(len(self.output))
        return gradient_activation
```
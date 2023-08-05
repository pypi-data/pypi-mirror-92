# NoxmainNetwork
# a Python3 module to create, train and test neural networks with mutiple layers
# by Noxmain
# -*- coding: utf-8 -*-
import numpy as np


def sigmoid(x):
    for y in range(len(x)):
        try:
            x[y, 0] = 1 / (1 + pow(3, -x[y, 0]))
        except OverflowError:
            x[y, 0] = round(x[y, 0], 10)
            x[y, 0] = 1 / (1 + pow(3, -x[y, 0]))
    return x


class NoxmainNetwork:
    def __init__(self, neurons, random=True, silent=False):
        """
        NoxmainNetwork(self, neurons, random=True, silent=False)
        Creates a neural network.

        Parameters
        ----------
        neurons: list
            Length of the list: number of layers.
            Values of list items: int > 1.
            Contains the neurons of the NoxmainNetwork. Each item is a layer with
            [itemvalue] neurons.
        random: bool, optional
            If true (default), the weights will be random when creating the
            NoxmainNetwork. Otherwise, every weight will be 0.0.
        silent: bool, optional
            If false (default), the NoxmainNetwork will print a message when loading
            or saving. Otherwise, it will not.
        """

        self.neurons = neurons
        self.silent = silent

        # Set weights
        lastneuron = 0
        self.weights = []

        for neuron in self.neurons:
            if lastneuron != 0:
                x = np.random.rand(neuron, lastneuron) * 2.0 - 1.0
                if not random:
                    for y in range(len(x)):
                        for z in range(len(x[y])):
                            x[y][z] = 0.0
                self.weights.append(x)
            lastneuron = neuron

    def train(self, inputs, targets, learningrate):
        """
        train(self, inputs, targets, learningrate)
        Trains the NoxmainNetwork.

        Parameters
        ----------
        inputs: list
            Length of list: number of neurons in the first layer (neurons[0]).
            Values of list items: float between 0.01 and 1.0.
        targets: list
            Length of list: number of neurons in the last layer (neurons[len(neurons) - 1]).
            Values of list items: float between 0.01 and 1.0.
        learningrate: float
            Value: between 0.01 and 1.0.
            Small learningrate: slower learning but more accurate results.
            Big learningrate: faster learning but more inaccurate results.
        """

        i = np.array(np.asfarray(inputs), ndmin=2).T
        t = np.array(np.asfarray(targets), ndmin=2).T

        o = [i]
        for weight in self.weights:
            i = sigmoid(np.dot(weight, i))
            o.append(i)

        # Calculate errors
        e = [t - i]
        laste = t - i
        for index in range(len(self.weights) - 1):
            e.append(np.dot(self.weights[(len(self.weights) - 1) - index].T, laste))
            laste = np.dot(self.weights[(len(self.weights) - 1) - index].T, laste)

        # Adjust weights
        for index in range(len(self.weights)):
            self.weights[index] += learningrate * np.dot((e[len(e) - (index + 1)] * o[index + 1] * (1.0 - o[index + 1])), o[index].T)

    def query(self, inputs):
        """
        query(self, inputs)
        Query the NoxmainNetwork.

        Parameters
        ----------
        inputs: list
            Length of list: number of neurons in the first layer (neurons[0]).
            Values of list items: float between 0.01 and 1.0.

        Returns
        -------
        o: list
            Length of list: number of neurons in the last layer (neurons[len(neurons) - 1]).
            Values of list items: float between 0.01 and 1.0.
            NoxmainNetwork outputs.
        """

        i = np.array(np.asfarray(inputs), ndmin=2).T

        for weight in self.weights:
            i = sigmoid(np.dot(weight, i))

        o = []
        for items in i:
            for item in items:
                o.append(item)

        return o

    def save(self, name, hide=False):
        """
        save(self, name)
        Saves the NoxmainNetwork as a .npy file in the same folder as
        this module.

        Parameters
        ----------
        name: string
            Filename: [name].npy
        hide: bool, optional
            If false (default), the file will be saved as named.
            Otherwise, a dot is appended to the front to hide the file.
        """

        save = [self.neurons, self.weights]
        prefix = ""
        if hide:
            prefix = "."
        np.save(str(prefix + name + ".npy"), save)

        if not self.silent:
            print("[NoxmainNetwork]: Network \"" + str(name) + "\" with neurons " + str(self.neurons) + " saved!")

    def load(self, name, hidden=False):
        """
        load(self, name)
        Loads the NoxmainNetwork from a .npy file in the same folder as
        this module.

        Parameters
        ----------
        name: string
            Filename: [name].npy
        hidden: bool, optional
            If false (default), it tries to load a visible file.
            Otherwise, it tries to load a hidden file. (Beginning with
            a dot)
        """

        prefix = ""
        if hidden:
            prefix = "."
        load = np.load(prefix + name + ".npy", encoding="latin1", allow_pickle=True)
        self.neurons = load[0]
        self.weights = load[1]

        if not self.silent:
            print("[NoxmainNetwork]: Network \"" + str(name) + "\" with neurons " + str(self.neurons) + " loaded!")

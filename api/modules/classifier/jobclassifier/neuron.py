from random import random
from math import exp
import logging


logging.basicConfig(level=logging.INFO)


class Neuron:
    def __init__(self, inputs):
        """
        Initialize neurons weights

        Weight for each input and one for the bias
        """
        self.log = logging.getLogger(__name__)
        self._inputs = inputs
        self._output = 0.0
        self._delta = 0.0
        self._activation = 0.0

        # Add bias as the last weight
        self._weights = [random() for _ in range(inputs+1)]
        self._velocity = [0] * inputs

        self.log.debug("CREATE: Weights {0}".format(self._weights))

    def activate(self, inputs):
        """
        Calculate activation of the neuron where last weight is the bias
        """
        self._activation = self._weights[-1]
        for i in range(len(self._weights[:-1])):
            self._activation += self._weights[i] * inputs[i]

    def transfer(self):
        """
        Sigmoid transfer function

        output = 1.0 / (1.0 + e^(-activation))
        """
        original_output = self._output
        try:
            self._output = 1.0 / (1.0 + exp(-self._activation))
        except Exception as e:
            self.log.error(e)
            self.log.debug(self._output)
            self.log.debug(self._activation)
            self._output = original_output
        return self._output

    def transfer_derivative(self):
        return self._output * (1.0 - self._output)

    def calc_error(self, index):
        return self._weights[index] * self._delta

    def calc_delta(self, error):
        self._delta = error * self.transfer_derivative()

    def update_weights(self, lrate, inputs):
        for j in range(len(inputs)):
            self._velocity[j] = 0.9 * self._velocity[j] + lrate * self._delta * inputs[j]
            self._weights[j] += self._velocity[j]

        self._weights[-1] += lrate * self._delta

    # Getters
    def output(self):
        return self._output

    def delta(self):
        return self._delta

    def export(self):
        return({
            "delta": self._delta,
            "inputs": self._inputs,
            "output": self._output,
            "weights": self._weights,
            "activation": self._activation
            })

    @classmethod
    def load(cls, settings):
        neuron = Neuron(settings['inputs'])
        neuron._delta = settings['delta']
        neuron._inputs = settings['inputs']
        neuron._output = settings['output']
        neuron._weights = settings['weights']
        neuron._activation = settings['activation']
        return neuron

    def __repr__(self):
        return "<neuron.Neuron weights: {}, bias: {}, output: {}".format(self._weights[:-1], self._weights[-1], self._output)

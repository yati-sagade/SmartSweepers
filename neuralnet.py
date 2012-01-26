'''
Created on Dec 30, 2011

@author: yati
'''
from utils import clamped_rand, sigmoid

class Neuron(object):
    '''The neuron class'''
    def __init__(self, num_inputs, weights=None):
        '''ctor: if weights are not explicitly given, clamped random values are
        used.'''
        if weights is not None:
            # The extra weight is for the bias 
            self.weights = weights[:] + [clamped_rand()]
            self.num_inputs = len(weights) + 1
        else:
            self.weights = [clamped_rand() for i in xrange(num_inputs + 1)]
            self.num_inputs = num_inputs + 1
    
    def excite(self, inputs, bias):
        '''applies the inputs and the bias given and returns the output'''
        if self.num_inputs != len(inputs) + 1:
            raise Exception("number of weights and number of inputs must match.")
        
        output = 0.0
        for i in xrange(self.num_inputs - 1):
            output += inputs[i] * self.weights[i]
        
        output += bias * self.weights[-1]
        
        return output
    

class NeuronLayer(list):
    '''encapsulates a Neuron Layer'''
    def __init__(self, num_neurons, num_inputs_per_neuron):
        '''This is a list subclass, so we append to self'''
        self.num_neurons = num_neurons
        self.num_inputs_per_neuron = num_inputs_per_neuron
        for i in xrange(num_neurons):
            self.append(Neuron(num_inputs_per_neuron))
    
    def excite(self, inputs, bias, filter_sigmoid=False):
        '''excites this layer with the inputs and the bias and returns the
        outputs as a tuple. if filter sigmoid is True, output from each neuron
        is filtered through the sigmoid response curve.'''
        outputs = []
        for n in self:
            res = n.excite(inputs, bias)
            if filter_sigmoid:
                res = sigmoid(res)    
            outputs.append(res)
        
        return outputs
    
class NeuralNet(list):
    '''The main net class - also a list subclass like NeuronLayer.'''
    def __init__(self, num_inputs, num_outputs, num_hidden, neurons_per_hidden):
        '''builds the net given the parameters - the bias is automatically
        added, and doesn't need to be accounted for by the caller.'''
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs
        self.neurons_per_hidden = neurons_per_hidden
        
        if num_hidden > 0:
            # At least one hidden layer
            # Create the first hidden layer, that has num_inputs inputs per
            # neuron.
            self.append(NeuronLayer(neurons_per_hidden, num_inputs))
            # Now, the other hidden layers:
            for i in xrange(num_hidden - 1):
                self.append(NeuronLayer(neurons_per_hidden, 
                                        neurons_per_hidden))
            # And finally, the output layer:
            self.append(NeuronLayer(num_outputs, neurons_per_hidden))
            
        else:
            # Just a single layer!
            self.append(NeuronLayer(num_outputs, num_inputs))
    
    def excite(self, inputs, bias, filter_sigmoid=False):
        outputs = reduce(lambda x, y: y.excite(x, bias, filter_sigmoid),
                         self,
                         inputs)
        
        return outputs
    
    def put_weights(self, weights):
        '''
        Takes an iterable consisting of weights - and successively assigns them
        to neurones one after the other, one layer after another starting from 
        the first hidden layer.
        '''
        wctr = 0
        for layer in self:
            for neuron in layer:
                for ip in xrange(neuron.num_inputs):
                    neuron.weights[ip] = weights[wctr]
                    wctr += 1
    
    def get_weights(self):
        weights = []
        for layer in self:
            for neuron in layer:
                for weight in neuron.weights:
                    weights.append(weight)
        
        return weights
    
    def get_num_weights(self):
        ret = 0
        for layer in self:
            for neuron in layer:
                ret += neuron.num_inputs
        
        return ret
    
                    
        
            
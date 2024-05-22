import numpy


class Brain():
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        self.weights_input_hidden = numpy.random.uniform(-1, 1, (self.hidden_nodes, self.input_nodes))
        self.weights_hidden_output = numpy.random.uniform(-1, 1, (self.output_nodes, self.hidden_nodes))

        self.bias_input_hidden = numpy.random.uniform(-1, 1, (self.hidden_nodes, 1))
        self.bias_hidden_output = numpy.random.uniform(- 1, 1, (self.output_nodes, 1))


    def forward(self, input_vector):
        x = numpy.array(input_vector, ndmin=2).T
        x = numpy.matmul(self.weights_input_hidden, x)
        x = numpy.add(x, self.bias_input_hidden)
        x = self.ReLU(x)
        x = numpy.matmul(self.weights_hidden_output, x)
        x = numpy.add(x, self.bias_hidden_output)
        x = self.sigmoid(x)
        return [val[0] for val in x]

    def ReLU(self, x):
        return numpy.maximum(0, x)

    def sigmoid(self, x):
        return 1 / (1 + numpy.exp(-x))
    
    def copy(self):
        copiedBrain = Brain(self.input_nodes, self.hidden_nodes, self.output_nodes)
        copiedBrain.weights_input_hidden = numpy.copy(self.weights_input_hidden)
        copiedBrain.weights_hidden_output = numpy.copy(self.weights_hidden_output)
        copiedBrain.bias_input_hidden = numpy.copy(self.bias_input_hidden)
        copiedBrain.bias_hidden_output = numpy.copy(self.bias_hidden_output)
        return copiedBrain

    def mutate(self, rate):
        rng = numpy.random.default_rng()
        def mutateFunction(x):
            if rng.random() < rate:
                return x + numpy.random.normal(0, 0.1)
            else:
                return x
        vectorized_mutate_function = numpy.vectorize(mutateFunction)

        self.weights_input_hidden = vectorized_mutate_function(self.weights_input_hidden)
        self.weights_hidden_output = vectorized_mutate_function(self.weights_hidden_output)
        self.bias_input_hidden = vectorized_mutate_function(self.bias_input_hidden)
        self.bias_hidden_output = vectorized_mutate_function(self.bias_hidden_output)
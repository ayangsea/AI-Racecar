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
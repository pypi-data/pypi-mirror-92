import numpy as np
from itertools import count

class Layer_Dense:
    _ids = count(1)
    _params= dict()#{}
    layer_activations= dict()#{}
    layers_num_arr = list()#[]

    def __init__(self, n_inputs, n_neurons, weight_type="random"):
        '''
        # Initialize weights and biases randomly
        @params :   n_inputs ---> number of features
                    n_neurons --> number of neurons
        '''


        self.layer_number = next(Layer_Dense._ids)
        Layer_Dense.layers_num_arr.append(self.layer_number)

        
        # Initializing the weights either random or zeros
        if weight_type == "random":
            self.weights = 0.1 * np.random.randn( n_neurons,n_inputs)
        elif weight_type == "zeros":
           self.weights = np.zeros(( n_neurons, n_inputs))

        self.biases = np.zeros((n_neurons, 1))

        # adding the initialized weight to _params dictionary
        Layer_Dense._params['W'+ str(self.layer_number)] = self.weights
        Layer_Dense._params['b'+ str(self.layer_number)] = self.biases
    def __del__(self):
        Layer_Dense._params.clear()
        Layer_Dense.layer_activations.clear()
        Layer_Dense.layers_num_arr.clear() #= 5#.clear()
        Layer_Dense._ids = count(1)


    #   passing data from activation function classes to Layer_Dens class
    def pass_act(self,act_type: str , A):
        """
        description 
        @Param: ---
        @Return: ---
        """
        Layer_Dense._params['A'+ str(self.layer_number)] = A
        Layer_Dense.layer_activations[self.layer_number] = act_type

    # multibly W*X and save them to out and _params dictionary
    def forward(self,inputs):
        if self.layer_number == 1: 
            Layer_Dense._params['A0'] = inputs
        self.out = np.dot(self.weights, inputs) + self.biases # Z

        return (self.out, self.weights,self.biases) 
        
    # get weights
    def get_weights(self):
        return self.weights

    # set weights and save them to _params dictionary
    def set_weights(self , new_weights):
        self.weights = new_weights
        Layer_Dense._params['W'+ str(self.layer_number)] = self.weights
        Layer_Dense._params['b'+ str(self.layer_number)] = self.biases

    def __reper__(self):
        pass

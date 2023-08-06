import numpy as np

class Linear:
    
    def __init__(self, n_inputs, n_neurons,l_size, weight_type="random_l"):
        '''
        # Initialize weights and biases randomly
        @params :   n_inputs ---> number of features
                    n_neurons --> number of neurons
        '''
        # Initializing the weights either random or zeros
        if weight_type == "random":
            self.weights = 0.1 * np.random.randn(n_neurons,n_inputs)
        elif weight_type == "random_l":
            self.weights = np.random.randn(n_neurons,n_inputs) * np.sqrt(2/l_size)     
        elif weight_type == "zeros":
           self.weights = np.zeros(( n_neurons, n_inputs))

        self.biases = np.zeros((n_neurons, 1))
   
    def forward(self,X):
        Z = np.dot(self.weights,X) + self.biases 
        return Z 

    def set_weights(self , new_weights):
        self.weights = new_weights

    def set_b(self,b):
        self.biases = b    
    def updateW_B(self,weights,bias):
        self.weights = weights 
        self.biases = bias
    def __reper__(self):
        return self.weights, self.biases
    def Values(self):
        return self.weights, self.biases

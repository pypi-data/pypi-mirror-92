import math
import numpy as np 

class Adam:
    def __inti__(self):
        pass
    @staticmethod
    def initialize_adam(parameters,layerlen):
        L = layerlen  # number of layers in the neural networks
        v = {}
        s = {}
        
        for l in range(L):
            v["dW" + str(l+1)] = np.zeros(parameters['W'+str(l+1)].shape)
            v["db" + str(l+1)] = np.zeros(parameters['b'+str(l+1)].shape)
            s["dW" + str(l+1)] = np.zeros(parameters['W'+str(l+1)].shape)
            s["db" + str(l+1)] = np.zeros(parameters['b'+str(l+1)].shape)
        
        return v, s
    @staticmethod   
    def update_parameters(layerlen,parameters, grads, v, s, t=2, learning_rate = 0.01,
                                beta1 = 0.9, beta2 = 0.999,  epsilon = 1e-8):
    
        L = layerlen                 # number of layers in the neural networks
        v_corrected = {}             # Initializing first moment estimate, python dictionary
        s_corrected = {}              # Initializing second moment estimate, python dictionary
        
        # Perform Adam update on all parameters
        for l in range(L):
            # Moving average of the gradients. Inputs: "v, grads, beta1". Output: "v".
            v["dW" + str(l+1)] = beta1*v["dW" + str(l+1)] + (1-beta1)*grads['dW' + str(l+1)]
            v["db" + str(l+1)] = beta1*v["db" + str(l+1)] + (1-beta1)*grads['db' + str(l+1)]

            # Compute bias-corrected first moment estimate. Inputs: "v, beta1, t". Output: "v_corrected".
            v_corrected["dW" + str(l+1)] = v["dW" + str(l+1)]/(1-np.power(beta1,t))
            v_corrected["db" + str(l+1)] = v["db" + str(l+1)]/(1-np.power(beta1,t))

            # Moving average of the squared gradients. Inputs: "s, grads, beta2". Output: "s".
            s["dW" + str(l+1)] = beta2*s["dW" + str(l+1)]+(1-beta2)*np.power(grads['dW' + str(l+1)],2)
            s["db" + str(l+1)] = beta2*s["db" + str(l+1)]+(1-beta2)*np.power(grads['db' + str(l+1)],2)

            # Compute bias-corrected second raw moment estimate. Inputs: "s, beta2, t". Output: "s_corrected".
            s_corrected["dW" + str(l+1)] = s["dW" + str(l+1)]/(1-np.power(beta2,t))
            s_corrected["db" + str(l+1)] = s["db" + str(l+1)]/(1-np.power(beta2,t))
            
            # Update parameters. Inputs: "parameters, learning_rate, v_corrected, s_corrected, epsilon". Output: "parameters".
            parameters["W" + str(l+1)] = parameters["W" + str(l+1)] - (learning_rate*v_corrected["dW" + str(l+1)]/
                                                            np.sqrt(s_corrected["dW" + str(l+1)]+epsilon))
            parameters["b" + str(l+1)] = parameters["b" + str(l+1)] - (learning_rate*v_corrected["db" + str(l+1)]/
                                                            np.sqrt(s_corrected["db" + str(l+1)]+epsilon))        

        return parameters
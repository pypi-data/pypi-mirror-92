import numpy as np
class momentum:
    '''
    " The class concerned The momentum optimization "
    '''

    def __init__(self,parameters):
        '''
        :param parameters: the Weights and biases of The current model
        '''
        self.parameters=parameters


    def velocity_preparation(self):
        '''
        :return: Velocity parameter for weights and biases as to update the parameters using momentum GD
        '''
        weights = len(self.parameters) // 2  # number of layers in the neural networks
        v = {}
        # Initialize velocity
        for w in range(weights):
            v["dW" + str(w + 1)] = np.zeros((self.parameters["W" + str(w + 1)].shape[0], self.parameters["W" + str(w + 1)].shape[1]))
            v["db" + str(w + 1)] = np.zeros((self.parameters["b" + str(w + 1)].shape[0], self.parameters["b" + str(w + 1)].shape[1]))
        return v


    def update_with_momentum(self,velocity,learning_rate,exponentially_weighted_average_parameter,gradients):
        '''
        :param velocity: Velocity of the gradient with momentum
        :param learning_rate: the learning rate
        :param exponentially_weighted_average_parameter: Beta , the momentum hyperparameter
        :param gradients: dW , dB , the gradients of the weights and biases of each layer
        :return: parameters: updated weights and biases
                 velocity : updated velocity to be used in the next iteration
        '''
        L = len(self.parameters) // 2  # number of layers in the neural networks
        for l in range(L):
            # compute velocities
             velocity["dW" + str(l + 1)] = exponentially_weighted_average_parameter * velocity["dW" + str(l + 1)] + (1 - exponentially_weighted_average_parameter) *  gradients['dW' + str(l + 1)]
             velocity["db" + str(l + 1)] = exponentially_weighted_average_parameter *  velocity["db" + str(l + 1)] + (1 - exponentially_weighted_average_parameter) * gradients['db' + str(l + 1)]
            # update parameters
             self.parameters["W" + str(l + 1)] = self.parameters["W" + str(l + 1)] -  learning_rate *  velocity["dW" + str(l + 1)]
             self.parameters["b" + str(l + 1)] = self.parameters["b" + str(l + 1)] -  learning_rate *  velocity["db" + str(l + 1)]

        return self.parameters, velocity




class ADAM:
    '''
    " The class concerned ADAM optimization technique "
    '''
    def __init__(self,parameters):
        '''
        :param parameters: The weights and biases for each layer before any updates
        '''
        self.parameters=parameters


    def adam_preparation(self):
        '''
        " Initialization of ADAM optimization's parameters"
        :return: EWA : exponentially weighted average parameter
                 RMS : Root mean square prop parameter
        '''
        L = len(self.parameters) // 2  # number of layers in the neural networks
        EWA = {}
        RMS = {}

        # Initialize v, s. Input: "parameters". Outputs: "v, s".
        for l in range(L):
            # exponentially weighted average parameters
            EWA["dW" + str(l + 1)] = np.zeros((self.parameters["W" + str(l + 1)].shape[0], self.parameters["W" + str(l + 1)].shape[1]))
            EWA["db" + str(l + 1)] = np.zeros((self.parameters["b" + str(l + 1)].shape[0], self.parameters["b" + str(l + 1)].shape[1]))
            # RMS prop average parameters
            RMS["dW" + str(l + 1)] = np.zeros((self.parameters["W" + str(l + 1)].shape[0], self.parameters["W" + str(l + 1)].shape[1]))
            RMS["db" + str(l + 1)] = np.zeros((self.parameters["b" + str(l + 1)].shape[0], self.parameters["b" + str(l + 1)].shape[1]))

        return EWA, RMS

    def update_with_adam(self,EWA,RMS,learning_rate,parameters,gradients,epoch_num,frist_beta=0.9,second_beta=0.995,epsilon=1e-8,):
        '''
        :param EWA: Exponentially weighted average parameter
        :param RMS: RMS prop parameter
        :param learning_rate: the learning rate
        :param parameters: weights and biases before update
        :param gradients: the Gradients of weights and biases for the current model's layers
        :param epoch_num: the Epoch number
        :param frist_beta: Beta_1 , the first hyperparameter for Exponentially weighted average's parameter
        :param second_beta:Beta_2 , the 2nd hyperparameter for RMS prop's parameter
        :param epsilon: The safety margin as to not divide by zero
        :return: :param parameters : The updated parameters of the current model
                 :param: EWA : the updated Exponentially weighted average parameters
                 :param RMS : the updated RMS prop parameters
        '''

        L = len(parameters) // 2  # number of layers in the neural networks
        EWA_corrected = {}  # Initializing first moment estimate, python dictionary
        RMS_corrected = {}  # Initializing second moment estimate, python dictionary

        # Perform Adam update on all parameters
        for l in range(L):

            EWA["dW" + str(l + 1)] = frist_beta * EWA["dW" + str(l + 1)] + (1 - frist_beta) * gradients['dW' + str(l + 1)]
            EWA["db" + str(l + 1)] = frist_beta * EWA["db" + str(l + 1)] + (1 - frist_beta) * gradients['db' + str(l + 1)]
            #EWA_corrected["dW" + str(l + 1)] = EWA["dW" + str(l + 1)] / ((1 - frist_beta ** epoch_num)+epsilon)
            #EWA_corrected["db" + str(l + 1)] = EWA["db" + str(l + 1)] / ((1 - frist_beta ** epoch_num)+epsilon)
            RMS["dW" + str(l + 1)] = second_beta * RMS["dW" + str(l + 1)] + (1 - second_beta) * np.square(gradients['dW' + str(l + 1)])
            RMS["db" + str(l + 1)] = second_beta * RMS["db" + str(l + 1)] + (1 - second_beta) * np.square(gradients['db' + str(l + 1)])
            #RMS_corrected["dW" + str(l + 1)] = RMS["dW" + str(l + 1)] / ((1 - second_beta ** epoch_num)+epsilon)
            #RMS_corrected["db" + str(l + 1)] = RMS["db" + str(l + 1)] / ((1 - second_beta ** epoch_num)+epsilon)
            parameters["W" + str(l + 1)] = parameters["W" + str(l + 1)] - learning_rate * EWA["dW" + str(l + 1)] / (np.sqrt(RMS["dW" + str(l + 1)]) + epsilon)
            parameters["b" + str(l + 1)] = parameters["b" + str(l + 1)] - learning_rate * EWA["db" + str(l + 1)] / (np.sqrt(RMS["db" + str(l + 1)]) + epsilon)


        return parameters, EWA,RMS

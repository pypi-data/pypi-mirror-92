import numpy as np
import back_prop
import Losses
class model_backward_general:
    '''
    " The Class which is concerned with combining the back propagation functions to form an integrated backprop model ."
    '''
    def __init__(self,Predictions,true_label,packet_of_packets,loss_function,lambd,activation_functions):
        '''
        :param Predictions: Y-hat --> the output of the activation function
        :param true_label: the true classes' values (labels)
        :param activation_functions : the type of activation function in each layer
        :param packet_of_packets: Tuple of 2 elements which will be used in backward propagation :
                     1- linear packer : contains ( input , weights , biases ) of the current layer
                     2- activation packet : contains ( Z ) which is the input to the activation function
        :param loss_function: type of the loss function
        :param lambd: regularization parameter
        :return : gradients of weights and biases
        '''
        self.lambd=lambd
        self.activation_functions = activation_functions
        self.predictions = Predictions
        self.Y = true_label
        self.packet_of_packets=packet_of_packets
        self.loss_function_type=loss_function
    def model_backward(self):
        gradients = {}
        L = len(self.packet_of_packets)  # the number of layers
        # m = self.predictions.shape[1]
        #  Y = self.Y.reshape(self.predictions.shape)  # after this line, Y is the same shape as AL

        # Initializing the backpropagation by getting the derivative of the cost function we are using wrt the output ( dl/dA )

        #  dAL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))  # derivative of cost with respect to AL
        #   dAL = np.mean(np.dot(X.T,(self.predictions-self.Y)))
        temp = back_prop.backward_model()
        current_cache = self.packet_of_packets[L - 1]

        # if (self.loss_function_type=="SSD"):
        #     temp_loss = Losses.square_difference(self.Y, self.predictions)
        #     dAL = temp_loss.backprop_cost(current_cache[0])
        # elif (self.loss_fuction_type=="LLH"):
        #     temp_loss = Losses.loglikelihood(self.Y, self.predictions)
        #     dAL = temp_loss.backprop_cost(current_cache[0])
        if (self.loss_function_type=="SSD"):
            temp_loss = Losses.square_difference(self.Y, self.predictions)
            dAL = temp_loss.backprop_cost(current_cache[0])
        elif (self.loss_function_type=="multiclass"):
            temp_loss = Losses.multiclass_loss(self.Y, self.predictions)
            dAL = temp_loss.backprop_cost(current_cache[0])

        gradients["dA" + str(L - 1)], gradients["dW" + str(L)], gradients["db" + str(L)] = temp.activation_backward(dAL,current_cache,"softmax",self.lambd)

        # Loop from l=L-2 to l=0
        for l in reversed(range(L - 1)):
            # lth layer: (RELU -> LINEAR) gradients.
            # Inputs: "grads["dA" + str(l + 1)], current_cache". Outputs: "grads["dA" + str(l)] , grads["dW" + str(l + 1)] , grads["db" + str(l + 1)]
            current_cache = self.packet_of_packets[l]
            dA_prev_of_l, dW_of_l, db_of_l = temp.activation_backward(gradients["dA" + str(l + 1)], current_cache, self.activation_functions[l-1],self.lambd)
            gradients["dA" + str(l)] = dA_prev_of_l
            gradients["dW" + str(l + 1)] = dW_of_l
            gradients["db" + str(l + 1)] = db_of_l

        return gradients

    '''
    def model_backward_with_droupout(self):
        gradients = {}
        #        linear_packet , activation_packet = self.packet_of_packets
        L = len(self.packet_of_packets)  # the number of layers
        # m = self.predictions.shape[1]
        #  Y = self.Y.reshape(self.predictions.shape)  # after this line, Y is the same shape as AL

        # Initializing the backpropagation by getting the derivative of the cost function we are using wrt the output ( dl/dA )

        #  dAL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))  # derivative of cost with respect to AL
        #   dAL = np.mean(np.dot(X.T,(self.predictions-self.Y)))
        # Lth layer (SIGMOID -> LINEAR) gradients. Inputs: "dAL, current_cache". Outputs: "grads["dAL-1"], grads["dWL"], grads["dbL"]
        # grads["dA" + str(L-1)], grads["dW" + str(L)], grads["db" + str(L)] = None
        temp = back_prop.backward_model()
        current_cache = self.packet_of_packets[L - 1]

        # if (self.loss_function_type=="SSD"):
        #     temp_loss = Losses.square_difference(self.Y, self.predictions)
        #     dAL = temp_loss.backprop_cost(current_cache[0])
        # elif (self.loss_fuction_type=="LLH"):
        #     temp_loss = Losses.loglikelihood(self.Y, self.predictions)
        #     dAL = temp_loss.backprop_cost(current_cache[0])
        if (self.loss_function_type == "SSD"):
            temp_loss = Losses.square_difference(self.Y, self.predictions)
            dAL = temp_loss.backprop_cost(current_cache[0])
        elif (self.loss_function_type == "multiclass"):
            temp_loss = Losses.multiclass_loss(self.Y, self.predictions)
            dAL = temp_loss.backprop_cost(current_cache[0])

        gradients["dA" + str(L - 1)], gradients["dW" + str(L)], gradients["db" + str(L)] = temp.activation_backward(dAL,current_cache,"softmax",self.lambd)

        # Loop from l=L-2 to l=0
        for l in reversed(range(L - 1)):
            # lth layer: (RELU -> LINEAR) gradients.
            # Inputs: "grads["dA" + str(l + 1)], current_cache". Outputs: "grads["dA" + str(l)] , grads["dW" + str(l + 1)] , grads["db" + str(l + 1)]
            current_cache = self.packet_of_packets[l]
            dA_prev_of_l, dW_of_l, db_of_l = temp.activation_backward(gradients["dA" + str(l + 1)], current_cache,"sigmoid", self.lambd)
            gradients["dA" + str(l)] = dA_prev_of_l
            gradients["dW" + str(l + 1)] = dW_of_l
            gradients["db" + str(l + 1)] = db_of_l

        return gradients
    '''

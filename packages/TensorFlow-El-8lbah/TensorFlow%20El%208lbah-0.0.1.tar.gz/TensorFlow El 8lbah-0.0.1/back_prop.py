import numpy as np
import Losses
import activations
class backward_model:
    '''
    " The class which is concerned with calculating the back propagation gradients , which will be used to update the
        weights and biases through the training process
    '''
    def identity_backward(self,dz,linear_packet,lambd):
        '''
        :param dz: The derivative of the loss w.r.t the input to the activation function (Z)
        :param linear_packet: a tuple which contains ( the input , weights and biases of the current layer )
        :param lambd: the Regularization parameter
        :return: - delta_input_previous , the gradient of the past input
                 - delta_w : gradient of the weights of the current layer
                 - delta_b : the gradient of the biases of the current layer
        '''
        A_prev, W, b = linear_packet
        m = A_prev.shape[1]
        if lambd:
            delta_w = (1 / m) * np.dot(dz, A_prev.T) + (lambd / m) * W  # derivative of loss w.r.t (w)
        else:
            delta_w = (1 / m) * np.dot(dz, A_prev.T)  # derivative of loss w.r.t (w)
        #delta_w =np.dot(dz, A_prev.T)  # derivative of loss w.r.t (w)
        delta_b = (1 / m) * np.sum(dz, axis=1, keepdims=True) # derivative of loss w.r.t (b)
        delta_input_prev = np.dot(W.T, dz)  # derivative of loss w.r.t (input)
        return delta_input_prev, delta_w, delta_b


    def activation_backward(self,delta_A,packet_of_packets, activation_type,lambd):
        '''
        :param delta_A: the derivative of the loss function w.r.t the activation function
        :param packet_of_packets: Tuple of 2 elements which will be used in backward propagation :
                     1- linear packer : contains ( input , weights , biases ) of the current layer
                     2- activation packet : contains ( Z ) which is the input to the activation function
        :param activation_type: the type of the activation function used in this layer
        :param lambd: regularization parameter
        :return: - delta_input_previous , the gradient of the past input
                 - delta_w : gradient of the weights of the current layer
                 - delta_b : the gradient of the biases of the current layer
        '''
        linear_packet, act_packet = packet_of_packets

        if activation_type == "relu":
            #print("hi")
            temp = activations.relu()
            dZ = temp.backaward(delta_A, act_packet)    # we have to implement this relu backward function
            dA_prev, dW, db = self.identity_backward(dZ,linear_packet,lambd)
        elif activation_type == "sigmoid":
            #print("hi")
            temp = activations.Sigmoid()
            dZ = temp.backward(delta_A, act_packet)
            dA_prev, dW, db = self.identity_backward(dZ,linear_packet,lambd)
        # we will start from here tomorrow , we have to deal with Y_hat , y_true while creating instance from cost class
       # temp = Losses.square_difference()
        #dA = temp.backprop_cost(self.linear_packet)
        elif activation_type == "softmax":
            temp = activations.Softmax()
            dZ = temp.diff(delta_A)
            dA_prev, dW, db = self.identity_backward(dZ, linear_packet,lambd)

        return dA_prev, dW, db



'''
dA = np.array([[0.208,0.613]]).T
z = np.array([[0.702,0.867]]).T
A = np.array([[0.808,0.604]]).T
W = np.array([[0.323,0.076],[0.614,0.106]]).T
b = np.array([[0.676,0.360]]).T
linear_packet = (A,W,b)
act_packet = z
packet_of_packets = linear_packet , act_packet
da_prev , dW , dB = backward_model().activation_backward(dA,packet_of_packets,"sigmoid")
print(f"da_prev = {da_prev} ")
print(f"dW = {dW} ")
print(f"db = {dB} ")
'''
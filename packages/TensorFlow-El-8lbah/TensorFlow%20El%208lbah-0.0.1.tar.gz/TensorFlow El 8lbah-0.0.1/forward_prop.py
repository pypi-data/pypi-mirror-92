import numpy as np
from layers import layers
import activations
class forward_prop:
    '''
    " This Class is Concerned with calculating the two parts of the forward propagation :
      identity part : calculating the product of the forward propagation before entering the activation function
      activation part : takes the output of the identity part and outputs the prediction based on the kind of the
                        activation function
    '''
    def identity_forward(self,X,W,b):
        '''
        :param X: the input of the current layer
        :param W: the weights of the current layer
        :param b: biases of the current layer
        :return: - The product of ( Weights * input ) + biases ,
                 - a Tuple which contains the Values of input , weights and biases of the current layer as to be used
                    in the backward propagation
        '''
        Z = np.dot(W, X) + b
       # print(Z)
        forward_packet = (X, W, b)
        return Z , forward_packet

    def activation_forward(self,input,W,b,activation_type):
        '''
        :param input: the input of the current layer
        :param W: the weights of the current layer
        :param b: biases of the current layer
        :param activation_type: Type of activation function used in the forward propagation
        :return: - A --> the output of the activation function
                 - packet_of_packets --> Tuple of 2 elements which will be used in backward propagation :
                     1- linear packer : contains ( input , weights , biases ) of the current layer
                     2- activation packet : contains ( Z ) which is the input to the activation function
        '''
        if activation_type == "sigmoid":
            Z, linear_packet = self.identity_forward(input, W, b) ## Z = input * w + b
            temp=activations.Sigmoid()
            A, activation_packet = temp.forward(Z) ## A = sig(z)

        elif activation_type == "relu":
            Z, linear_packet = self.identity_forward(input, W, b)
            temp = activations.relu()
            A, activation_packet = temp.forward(Z)

        elif activation_type == "leaky_relu":
            Z, linear_packet = self.identity_forward(input, W, b)
            temp = activations.leaky_relu()
            A, activation_packet = temp.forward(Z)
        elif activation_type == "tanh":
            Z, linear_packet = self.identity_forward(input, W, b)
            temp = activations.tanh()
            A, activation_packet = temp.forward(Z)
        elif activation_type == "softmax":
            Z, linear_packet = self.identity_forward(input, W, b)
            #temp =
            A, activation_packet = activations.Softmax().forward(Z)
        elif activation_type == "linear":
            Z, linear_packet = self.identity_forward(input, W, b)
            # temp =
            A, activation_packet = Z,Z

        else:
            raise ValueError("ERROR : Activation Function is Not Determined")

        packet_of_packets = linear_packet, activation_packet
        return A, packet_of_packets
    '''
    def activation_forward_with_droupout(self, input, W, b, droupouRatio,activation_type):
        if activation_type == "sigmoid":
            Z, linear_packet = self.identity_forward(input, W, b)  ## Z = input * w + b
            temp = activations.Sigmoid()
            A, activation_packet = temp.forward(Z)  ## A = sig(z)
            droup = np.random.randn(A.shape[0], A.shape[1])
            droup = (droup < droupouRatio)
            A = A * droup
            A = A / droupouRatio
            activation_packet = Z, droup

        elif activation_type == "relu":
            Z, linear_packet = self.identity_forward(input, W, b)
            temp = activations.relu()
            A, activation_packet = temp.forward(Z)
            droup=np.random.randn(A.shape[0],A.shape[1])
            droup=(droup<droupouRatio)
            A=A*droup
            A=A/droupouRatio
            activation_packet = Z,droup

        elif activation_type == "leaky_relu":
            Z, linear_packet = self.identity_forward(input, W, b)
            temp = activations.leaky_relu()
            A, activation_packet = temp.forward(Z)
            droup = np.random.randn(A.shape[0], A.shape[1])
            droup = (droup < droupouRatio)
            A = A * droup
            A = A / droupouRatio
            activation_packet = Z, droup

        elif activation_type == "tanh":
            Z, linear_packet = self.identity_forward(input, W, b)
            temp = activations.tanh()
            A, activation_packet = temp.forward(Z)
            droup = np.random.randn(A.shape[0], A.shape[1])
            droup = (droup < droupouRatio)
            A = A * droup
            A = A / droupouRatio
            activation_packet = Z, droup

        elif activation_type == "softmax":
            droupouRatio=1
            Z, linear_packet = self.identity_forward(input, W, b)
            # temp =
            A, activation_packet = activations.Softmax().forward(Z)
            droup = np.random.randn(A.shape[0], A.shape[1])
            droup = (droup < droupouRatio)
            A = A * droup
            A = A / droupouRatio
            activation_packet = Z, droup

        else:
            raise ValueError("pierre Was here")

        packet_of_packets = linear_packet, activation_packet
        return A, packet_of_packets

    '''
'''
test_cases=forward_prop()
np.random.seed(1)
A = np.random.randn(3, 2)
W = np.random.randn(1, 3)
b = np.random.randn(1, 1)
Z , forward_packet = test_cases.identity_forward(A,W,b)
print(forward_packet)
'''
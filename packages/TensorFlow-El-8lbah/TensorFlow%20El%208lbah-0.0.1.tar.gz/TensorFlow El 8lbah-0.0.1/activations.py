import numpy as np

import matplotlib.pyplot as plt

class Sigmoid:
    '''
    "The class concerned the Sigmoid function which will calculate it and it's derivative for the sake of forward
                and backward propagation respectively . "
    '''
    def forward(self, z):
        '''

        :param z: The result of multiplying ( Weight * input ) + bias
        :return: The sigmoid of the input
        '''
        sig = 1 / (1 + np.exp(-z))
        act_packet = z
        return sig, act_packet

    def derivative(self,z):
        '''
        :param z: The sigmoid input
        :return: The shortcut result of the derivative of the sigmoid function
        '''
        sig = 1 / (1 + np.exp(-z))
        return sig*(1-sig)
    def backward(self,dA,act_packet):
        '''

        :param dA: Derivative of the Loss function with respect the sigmoid function
        :param act_packet: The value of the Z , which is the output before entering the activation function
        :return:
        '''
        #derivative_of_sigmoid = self.derivative(act_packet)
        #dz=np.multiply(dA,derivative_of_sigmoid)
        #test = np.ones_like(dz)
        return dA




# backward activation here #

class relu:
    '''
    The class concerned the relu function which will calculate it and it's derivative for the sake of forward
                and backward propagation respectively .
    '''
    def forward(self, z):
        '''

        :param z: The relu input
        :return: the relu output for the input
        '''
        rel = np.maximum(0, z)
        act_packet = z
        return rel, act_packet
# backward action here
    def backaward(self,dLA, activation_packet):
        '''

        :param dLA: Derivative of the Loss function with respect the relu function
        :param activation_packet: The value of the Z , which is the output before entering the activation function
        :return: the derivative of the cost function with respect to Z
        '''

        Z = activation_packet
        #print("Z")
        #print(Z.shape)
        dZ = np.array(dLA, copy=True)  # just converting dz to a correct object.

        # When z <= 0, you should set dz to 0 as well.
        #dZ[Z<=0] = 0
        dZ = np.where(Z>0,1,0)
        assert (dZ.shape == Z.shape)
        return dZ
      #  print(type(Z))
        #dZ = np.array(dLA, copy=True)  # just converting dz to a correct object.
     #   print(type(dZ))
        # dl/dz = dl/da * da/dz .. as da/dz = 1 if the z > 0 when we are using relu activation function when z>0 , so dl/dz = dl/da if z>0
        # but if z<=0 so da/dz will equal 0 then dl/dz = 0
        # When z <= 0, you should set dz to 0 as well.


class leaky_relu:
    '''
    The class concerned the leaky_relu function which will calculate it and it's derivative for the sake of forward
                and backward propagation respectively .
    '''
    def forward(self,z):
        '''

        :param z: the leaky_relu input
        :return: the leaky_relu output of the input
        '''
        y1 = ((z > 0) * z)
        y2 = ((z <= 0) * z * 0.01)
        leaky= y1 + y2
        act_packet = z
        return leaky , act_packet

    def backaward(self, dLA, activation_packet):
        '''
        :param dLA: Derivative of the Loss function with respect the leaky_relu function
        :param activation_packet: The value of the Z , which is the output before entering the activation function
        :return: the derivative of the cost function with respect to Z
        '''

        Z = activation_packet
        # print("Z")
        # print(Z.shape)
        dZ = np.array(dLA, copy=True)  # just converting dz to a correct object.

        # When z <= 0, you should set dz to 0 as well.
        dZ[Z <= 0] = 0
        # dZ = np.where(Z>0,1,0)
        assert (dZ.shape == Z.shape)
        return dZ

class tanh:
    '''
     The class concerned the tanh function which will calculate it and it's derivative for the sake of forward
                and backward propagation respectively .
    '''
    def forward(self,z):
        '''
        :param z: the tanh input
        :return: the tanh output of the input
        '''
        TANH = np.tanh(z)
        act_packet = z
        return TANH , act_packet
    def diff(self,z):
        '''
        :param z : the input to the tanh function
        :return : the backward shortcut result of the derivative of the tanh function w.r.t the Z
        '''
        tanh=self.forward(z)
        return (1-np.square(tanh))
    def backward(self,dA,act_packet):
        '''

        :param dA: Derivative of the Loss function with respect the tanh function
        :param act_packet: The value of the Z , which is the output before entering the activation function
        :return: the derivative of the cost w.r.t  Z ( dL/dZ = dL/dA * dA/dZ )
        '''
        derivative_of_tanh = self.diff(act_packet)
        dz=np.multiply(dA,derivative_of_tanh)
        #test = np.ones_like(dz)
        return dz

class Softmax():
    '''
    '''
    def forward(self, z):
        '''
        :param z: the input to the softmax function
        :return: the forward output of the softmax activation function
        '''
        act_packet = z
        ans = np.exp(z - np.max(z))
        ans = ans / ans.sum(axis=0)
        return ans, act_packet


    def diff(self,dA):
        '''
        :param dA: derivative of Loss w.r.t the output of the softmax activation function
        :return: the derivative of the loss w.r.t Z --> the output before entering the activation function
        '''
        #dA = np.ones(z.shape)
        #m, n = z.shape
        #p = self.__call__(z)
        #tensor1 = np.einsum('ij,ik->ijk', p, p)  # (m, n, n)
        #tensor2 = np.einsum('ij,jk->ijk', p, np.eye(n, n))  # (m, n, n)
        #dz = tensor2 - tensor1
        #dz = np.einsum('ijk,ik->ij', dz, dA)
        #return dz
        return dA

'''
dummy=(np.arange(100)/10)-5
test_sigmoid = tanh()
result , act = test_sigmoid.forward(dummy)
#print(result)
plt.plot(dummy,result)
plt.show()
'''
'''
dummy=[3.1, -9.3, 7, 8.7, 3.6, 5.2, 4.7, -2.2, 3.1, -6.6]
test_soft_max=softmax()
result , act_packet = test_soft_max.forward(dummy)
print(result)
'''
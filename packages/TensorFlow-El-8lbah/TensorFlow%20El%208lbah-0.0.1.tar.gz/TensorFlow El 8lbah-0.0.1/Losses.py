import numpy as np
class square_difference():
    '''
    "This is the class which is Concerned with Calculating the SSD loss & it's derivative "
    '''
    def __init__(self,true_label,Y_hat):
        '''
        :param true_label: The true classes of the input training examples
        :param Y_hat: the output of the forward propagation .. the prediction of Training .. the output from the
                        activation function
        '''
        self.true_label=true_label
        self.Y_hat=Y_hat
    def cost(self):
        '''
        :return: The value of the cost using the SSD Loss function
        '''
        #cost =0.5 * np.mean(np.dot(np.transpose((self.true_label - self.Y_hat)), (self.true_label - self.Y_hat)) * (1/self.true_label.shape[0]))
        m = self.true_label.shape[1]
        #print(self.Y_hat.shape)
        logprobs = np.multiply(-np.log(self.Y_hat), self.true_label) + np.multiply(-np.log(1 - self.Y_hat), 1 - self.true_label)
        cost = 1. / m * np.nansum(logprobs)
        #cost = np.nansum(logprobs)
        return cost
    def backprop_cost(self,cache):
        '''
        :param cache: a tuple which contains the values of ( input , weight , bias ) of the current layer
        :return: returns the back propagation loss value for back propagation calculations
        '''
        X , W , b = cache
        #def_cost = np.mean(np.dot(X,(self.Y_hat-self.true_label).T))
        def_cost = self.Y_hat - self.true_label
        return def_cost     # dA

class regularization:
    '''
    "Implementing the cost function with L2 regularization."
    '''
    def compute_cost_with_regularization(self,prediction, Y, parameters, lambd,loss_type):
        '''
        :param prediction  -- post-activation, output of forward propagation, of shape (output size, number of examples)
        :param Y -- "true" labels vector, of shape (output size, number of examples)
        :param parameters -- python dictionary containing parameters of the model
        :return: cost - value of the regularized loss function (formula (2))
        '''
        m = Y.shape[1]
        x=0
        temp = len(parameters) //2
        if (loss_type=="SSD"):
            #print("hi")
            cross_entropy_cost = square_difference(Y,prediction).cost()  # This gives you the cross-entropy part of the cost
        elif (loss_type=="multiclass"):
                # print("hi")
                cross_entropy_cost = multiclass_loss(Y,prediction).cost()  # This gives you the cross-entropy part of the cost
        for i in range(1,temp):
           x=+np.sum(np.square (parameters["W"+str(i)]))
        ### START CODE HERE ### (approx. 1 line)
        L2_regularization_cost = lambd / (2 * m) * x
        ### END CODER HERE ###

        cost = cross_entropy_cost + L2_regularization_cost

        return cost
class loglikelihood():
    '''
    "This is the class which is Concerned with Calculating the loglikelihood loss & it's derivative "
    '''
    def __init__(self, true_label, Y_hat):
        '''
       :param true_label: The true classes of the input training examples
       :param Y_hat: the output of the forward propagation .. the prediction of Training .. the output from the
                        activation function
        '''
        self.true_label = true_label
        self.Y_hat = Y_hat
    def cost(self):
        '''
         :return: The value of the cost using the loglikelihood Loss function
        '''
        cost = 0.5*(np.mean(-1*np.log(np.abs((self.true_label/2)-0.5+self.Y_hat))))
        return cost
    def backprop_cost(self,cache):
        '''
        :param cache: a tuple which contains the values of ( input , weight , bias ) of the current layer
        :return: returns the back propagation loss value for back propagation calculations
        '''
        X , W , b = cache
        def_cost= np.mean((np.dot(-1*self.Y_hat*X)/(1+np.exp(np.dot(self.true_label,self.Y_hat)))))
        return def_cost



class multiclass_loss():
    '''
    "This is the class which is Concerned with Calculating the multiclass loss & it's derivative "
    '''
    def __init__(self, Y, Y_hat):
        '''
        :param true_label: The true classes of the input training examples
        :param Y_hat: the output of the forward propagation .. the prediction of Training .. the output from the
                              activation function
        '''
        self.Y = Y
        self.Y_hat = Y_hat
    def cost(self):
        '''
        :return: The value of the cost using the multiclass Loss function
        '''
        #m = self.Y.shape[1]
       # logprobs = np.multiply(-np.log(self.Y_hat), self.Y) + np.multiply(-np.log(1 - self.Y_hat), 1 - self.Y)
        #cost = 1. / m * np.nansum(logprobs)
        cost = -(1/ self.Y.shape[1]) * np.sum(np.multiply(self.Y, np.log(self.Y_hat)))
        return cost
    
    def backprop_cost(self,cache):
        '''
        :param cache: a tuple which contains the values of ( input , weight , bias ) of the current layer
        :return: returns the back propagation loss value for back propagation calculations
        '''
        X , W , b = cache
        #def_cost = np.mean(np.dot(X,(self.Y_hat-self.true_label).T))
        def_cost = self.Y_hat - self.Y
        return def_cost  



class identity_loglikelihood():
    '''
    "The class which is concerned with calculating the loglikelihood loss function with identity activation function"
    '''
    def __init__(self, true_label, Y_hat):
        '''
        :param true_label: The true classes of the input training examples
        :param Y_hat: the output of the forward propagation .. the prediction of Training .. the output from the
                                      activation function
        '''
        self.true_label = true_label
        self.Y_hat = Y_hat
    def cost(self):
        '''
        :return: the Cost value of the loglikelihood loss with an identity activation
        '''
        cost =  (np.mean(np.log(1+(np.exp(-1*self.true_label*self.Y_hat)))))
        return cost


class perceptron_model_loss():
    '''
    "The perceptron criteria loss Class"
    '''
    def __init__(self, true_label, Y_hat):
        '''
        :param true_label: The true classes of the input training examples
        :param Y_hat: the output of the forward propagation .. the prediction of Training .. the output from the
                                              activation function
        '''
        self.true_label = true_label
        self.Y_hat = Y_hat
    def cost(self):
        '''
        :return: the Cost value of the perceptron model loss with an identity activation
        '''
        cost = np.argmax(0,-1*np.dot(self.true_label,self.Y_hat))
        return cost


class hinge_loss():
    '''
    "The hinge_loss (SVM) loss Class"
    '''
    def __init__(self, true_label, Y_hat):
        '''
        :param true_label: The true classes of the input training examples
        :param Y_hat: the output of the forward propagation .. the prediction of Training .. the output from the
                                                      activation function
        '''
        self.true_label = true_label
        self.Y_hat = Y_hat
    def cost(self):
        '''
        :return : the Cost value of the loss with an identity activation
        '''
        cost = np.argmax(0,(-1*np.dot(self.true_label,self.Y_hat))+1)
        return cost

'''
y_hat=np.array([0.5,0.35,0.83,0.73])
#y_hat=y_hat.T
labels=np.array([1,1,1,-1])
test_loss=loglikelihood(labels,y_hat)
print(test_loss.cost())
'''
'''
y_hat=np.array([0,-0.6,1.6,1])
#y_hat=y_hat.T
labels=np.array([1,1,1,-1])
test_loss=identity_loglikelihood(labels,y_hat)
print(test_loss.cost())
'''
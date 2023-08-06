import matplotlib.pyplot as plt
import matplotlib.animation as animation
import layers  , forward_model , Losses , backward_model
from dataset import dataset
from Metric import evaluation_metrics
from matplotlib import style
import shelve
import matplotlib; matplotlib.use("TkAgg")
style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
class training_model:
    '''
    " The Training class using batch gradient descent "
    '''
    def __init__(self,X, Y,layers_dimenstions,activation_functions, alpha=0.5 , no_of_iterations=60, print_cost = True, lambd = 0  ):
        '''
        :param X: The input of the first layer
        :param Y: the True labels of the training examples
        :param layers_dimenstions : the number of hidden units in each hidden layer
        :param activation_functions : the type of activation function in each hidden layer
        :param alpha: learning rate
        :param no_of_iterations: number of iterations
        :param print_cost: boolean variable , put it with ( True ) value if you want to print the cost every 10
                        iterations
        :param lambd: regularization parameter

        :return : The Trained Parameters for a certain model trained on a certain dataset
        '''
        self.input = X
        self.Y=Y
        self.learning_rate = alpha
        self.no_of_iterations = no_of_iterations
        self.print_cost=print_cost
        self.regularization_parameter=lambd
        self.dimension_layers = layers_dimenstions
        self.activation_functions = activation_functions

    def update_parameters(self,parameters, grads, learning_rate):
        '''
          "The function which is used to update the weights and biases of the model with Vanilla Gradient descent ."
        :param parameters: weights and biases of the past iteration ( before updating )
        :param grads: the Gradients of the weights and biases , the output of the backward propagation
        :param learning_rate: The learning rate
        :return: parameters : updated weights and biases after completing one iteration of the training
        '''
        L = len(parameters) // 2  # number of layers in the neural network
        for l in range(L):
            parameters["W" + str(l + 1)] = parameters["W" + str(l + 1)] - learning_rate * grads["dW" + str(l + 1)]
            parameters["b" + str(l + 1)] = parameters["b" + str(l + 1)] - learning_rate * grads["db" + str(l + 1)]

        return parameters

    def animate(i):
        '''
        "A function which is used to draw a live plotting of the Cost function during the training process "
        '''

        graph_data = open('costs.txt', 'r').read()
        lines = graph_data.split('\n')
        xs = []
        ys = []

        # plt.title("Learning rate =" + str(self.learning_rate))
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(float(x))
                ys.append(float(y))
        ax1.clear()
        plt.ylabel('cost')
        plt.xlabel('iterations')
        ax1.plot(xs, ys)



    def save_model(self, filename):
        """Saves model by its name in the directory specified."""

        with shelve.open(filename) as db:
            db['self'] = self

    def train(self):

        '''
         " This function considered as the integration of all the past Modules together to start training any model
           the deep learning engineer will have the option to choose :
           1- the layers dimensions
           2- the activation function of each layer
           3- the loss type
           4- the number of iterations
          this function will plot live graph for the training cost and finally will print the the accuracy resulted
           from the test set training using the parameters resulted from the training set training .
        :return: The Trained parameters
        '''


        temp_layers= layers.layers(self.dimension_layers)
        # Initialize parameters dictionary.
        parameters = temp_layers.layers_init()
        #print (parameters)
        #print (parameters)
        #print("weights:")
        #print(parameters["W3"].shape)

        # Loop (gradient descent)
        cost_file = open("costs.txt", 'a+')
        cost_file.truncate(0)
        cost_file.close()
        for i in range(0,self.no_of_iterations):
            predictions, packet_of_packets = forward_model.forward_model().forward_model(self.input,parameters,self.activation_functions)
            #print(predictions.shape)
            #print (predictions)

            # Cost function
            if self.regularization_parameter == 0:
                cost =Losses.multiclass_loss(self.Y,predictions).cost()
                #print(cost)
            else:
                cost = Losses.regularization.compute_cost_with_regularization(predictions, self.Y, parameters, self.regularization_parameter,"multiclass")

            # Backward propagation.
            grads = backward_model.model_backward_general(predictions, self.Y, packet_of_packets, "multiclass",self.regularization_parameter,self.activation_functions).model_backward()
            # Update parameters.
            parameters = self.update_parameters(parameters, grads, self.learning_rate)
            # plot the cost
            #costs.append(cost)
            #self.visualize_cost(i,cost)
           # ani = animation.FuncAnimation(self.fig,self.draw,interval=1000)
            #plt.show()
            cost_file = open("costs.txt", 'a+')
            cost_file.write(f"{i},{cost} \n")
            cost_file.close()
            plt.ion()
            plt.ylabel('cost')
            plt.xlabel('iterations')
            plt.title("Learning rate =" + str(self.learning_rate))
            plt.show()
            plt.draw()
            plt.pause(1)
            '''
            plt.figure()
            plt.plot(costs)
            plt.ylabel('cost')
            plt.xlabel('iterations')
            plt.title("Learning rate =" + str(self.learning_rate))
            plt.show()
            '''
            # Print the loss every 10000 iterations
            if self.print_cost and i % 10 == 0:
                print("Cost after iteration {}: {}".format(i, cost))
        '''
        # plot the cost
        plt.figure()
        plt.plot(costs)
        plt.ylabel('cost')
        plt.xlabel('iterations')
        plt.title("Learning rate =" + str(self.learning_rate))
        plt.show()
        '''
        return parameters


def load_model(filename):
    """Loads a model saved in 'filename'."""

    with shelve.open(filename) as db:
        model = db['self']
    return model



if __name__ == "__main__":
    ani = animation.FuncAnimation(fig, training_model.animate, interval=1000)
    data_set = dataset('mnist', r'C:\Users\FacultyStudent\PycharmProjects\final_NN')
    train_X, train_Y, test_X, test_Y = data_set.get_dataset()
    temp = train_Y
    # print(train_Y.shape)
    train_Y = data_set.labels_to_onehot(train_Y)
    layers_dimensions = [train_X.T.shape[0], 128, train_Y.shape[0]]
    # print((train_X.shape))
    # print((train_Y.shape))
    # print(train_X.shape)
    # print(test_X.shape)
    # print(train_Y.shape)
    # print(test_Y.shape)
    # print("x_dimensions")
    # print(train_X.shape)
    # print("y_label:")
    # print(train_Y.shape)
    activation_functions = ["NONE", "sigmoid", "sigmoid"]
    parameters = training_model(train_X.T, train_Y, layers_dimensions, activation_functions).train()
    training_model(train_X.T, train_Y, layers_dimensions, activation_functions).save_model("test")
   # dectionary = training_model(train_X.T, train_Y, layers_dimensions, activation_functions).load_model("test.dir")
    dectionary = load_model("test.bak")
    print(dectionary)
    # parameters = training_model(X_train, Y_train).train()
    temp = evaluation_metrics(temp, train_X.T, parameters,activation_functions).Accuracy(train_X.shape[0])
    print(f"our accuracy : {temp} ")

    # print ("On the training set:")
    # predictions_train = predict(train_X.T, train_Y.T, parameters)
    # predictions_train = predict(train_X.T, train_Y, parameters)

    # print ("On the test set:")
    # predictions_test = predict(test_X.T, test_Y, parameters)
    # predictions_test = predict(X_test, Y_test, parameters)

    '''
    plt.title("Model without regularization")
    axes = plt.gca()
    axes.set_xlim([-0.75,0.40])
    axes.set_ylim([-0.75,0.65])
    plot_decision_boundary(lambda x: predict_dec(parameters, test_X.T), train_X, train_Y)
    '''

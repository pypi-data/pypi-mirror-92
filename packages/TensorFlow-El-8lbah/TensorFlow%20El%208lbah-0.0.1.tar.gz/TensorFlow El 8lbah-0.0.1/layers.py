from init import initialization
class layers():
    '''
    This Class was just to keep the naming convention of the models , this will use the init function to get the weights
                & biases of the hidden layers .
    '''
    def __init__(self,layers_dimensions):
        self.layers_dimensions=layers_dimensions
        '''
                    " This function will initialize a random values for weights and zeros for biases using the
                                dimension_layers list "

                    :type layers_dimensions: list
                    :param layers_dimensions: list of the number of hidden units in each hidden layer . 

        '''
    def layers_init(self): # [5,4,6,7,1]
        init=initialization(self.layers_dimensions)
        return init.initialize_parameters()

'''
inputs = [1,6,4,7,1]
layerrrrrr=layers(inputs)
parameters = layerrrrrr.layers_init()
print(parameters)
'''
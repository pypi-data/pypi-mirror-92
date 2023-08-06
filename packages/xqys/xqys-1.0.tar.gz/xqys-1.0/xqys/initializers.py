import numpy as np

class Zeros:
    '''Initializer generates numpy arrays initialized with zeros.
    '''
    @staticmethod
    def initialize_parameters(layers_dims):
        '''initializes parameters.

        Args:
            layers_dims: list of the dimentions of the neural network.
        Returns:
            dictionary of the initialized parameters.
        '''

        num_layers = len(layers_dims)
        parameters = {}
        
        for l in range(1, num_layers):
            parameters[f'W{l}'] = np.zeros(layers_dims[l], layers_dims[l-1])
            parameters[f'b{l}'] = np.zeros((layers_dims[l], 1))
            
            assert(parameters[f'W{l}'].shape == (layers_dims[l], layers_dims[l-1]))
            assert(parameters[f'b{l}'].shape == (layers_dims[l], 1))
        
        return parameters

class Ones:
    '''Initializer generates numpy arrays initialized with ones.
    '''
    @staticmethod
    def initialize_parameters(layers_dims):
        '''initializes parameters.

        Args:
            layers_dims: list of the dimentions of the neural network.
        Returns:
            dictionary of the initialized parameters.
        '''

        num_layers = len(layers_dims)
        parameters = {}
        
        for l in range(1, num_layers):
            parameters[f'W{l}'] = np.ones(layers_dims[l], layers_dims[l-1])
            parameters[f'b{l}'] = np.zeros((layers_dims[l], 1))
            
            assert(parameters[f'W{l}'].shape == (layers_dims[l], layers_dims[l-1]))
            assert(parameters[f'b{l}'].shape == (layers_dims[l], 1))
        
        return parameters


class He:
    '''Initializer generates numpy arrays initialized using He normal.
    '''
    def __init__(self, seed=None):
        self.seed = seed

    def initialize_parameters(self, layers_dims):
        '''initializes parameters.

        Args:
            layers_dims: list of the dimentions of the neural network.
        Returns:
            dictionary of the initialized parameters.
        '''

        if self.seed:
            np.random.seed(self.seed)
        num_layers = len(layers_dims)
        parameters = {}
        
        for l in range(1, num_layers):
            parameters[f'W{l}'] = np.random.randn(layers_dims[l], layers_dims[l-1]) * np.sqrt(2.0 / layers_dims[l-1])
            parameters[f'b{l}'] = np.zeros((layers_dims[l], 1))
            
            assert(parameters[f'W{l}'].shape == (layers_dims[l], layers_dims[l-1]))
            assert(parameters[f'b{l}'].shape == (layers_dims[l], 1))

        return parameters

class RandomNormal:
    '''Initializer generates numpy arrays with normal distribution.
    '''
    def __init__(self, mean=0.0, stddev=0.05, seed=None):
        self.seed = seed
        self.mean = mean
        self.stddev = stddev

    def initialize_parameters(self, layers_dims):
        '''initializes parameters.

        Args:
            layers_dims: list of the dimentions of the neural network.
        Returns:
            dictionary of the initialized parameters.
        '''

        if self.seed:
            np.random.seed(self.seed)
        num_layers = len(layers_dims)
        parameters = {}
        
        for l in range(1, num_layers):
            parameters[f'W{l}'] = np.random.normal(self.mean, self.stddev,  (layers_dims[l], layers_dims[l-1]))
            parameters[f'b{l}'] = np.zeros((layers_dims[l], 1))
            np.random.normal(3, 2.5, size=(2, 4))
            assert(parameters[f'W{l}'].shape == (layers_dims[l], layers_dims[l-1]))
            assert(parameters[f'b{l}'].shape == (layers_dims[l], 1))

        return parameters


        
class RandomUniform:
    '''Initializer generates numpy arrays with uniform distribution.
    '''
    def __init__(self, minval=-0.05, maxval=0.05, seed=None):
        self.seed = seed
        self.minval = minval
        self.maxval = maxval

    def initialize_parameters(self, layers_dims):
        '''initializes parameters.

        Args:
            layers_dims: list of the dimentions of the neural network.
        Returns:
            dictionary of the initialized parameters.
        '''

        if self.seed:
            np.random.seed(self.seed)
        num_layers = len(layers_dims)
        parameters = {}
        
        for l in range(1, num_layers):
            parameters[f'W{l}'] = np.random.uniform(self.minval, self.maxval,  (layers_dims[l], layers_dims[l-1])) 
            parameters[f'b{l}'] = np.zeros((layers_dims[l], 1))
            np.random.normal(3, 2.5, size=(2, 4))
            assert(parameters[f'W{l}'].shape == (layers_dims[l], layers_dims[l-1]))
            assert(parameters[f'b{l}'].shape == (layers_dims[l], 1))

        return parameters
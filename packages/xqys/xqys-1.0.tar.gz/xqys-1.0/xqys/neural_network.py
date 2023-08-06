import numpy as np
import math
import matplotlib.pyplot as plt
import pickle

from xqys.activation_functions import get_activation, activation_backward
from xqys.cost_functions import compute_cost, grad_cost, compute_reg_cost
from xqys.metrics import compute_score


class NeuralNet:
    '''Class implements a Neural Network.
    '''
    def __init__(self):

        self.layers_dims = [None]
        self.activations = []
        self.L2_regularization_lambdas = []

        self.parameters = {}
 

    def add_dense_layer(self, units, activation, L2_regularization_lambda=None):
        '''addes dense layer.

        Args:
            units: number of neurons.
            activation: the activation function.
            L2_regularization_lambda: the lambda if wanted to use L2 reg at this layer

        The activation functions supported are (sigmoid, relu, prelu, elu, tanh, arctan, identity, binary-step)
        '''
        self.layers_dims.append(units)
        self.activations.append(activation)
        self.L2_regularization_lambdas.append(L2_regularization_lambda)

    @staticmethod
    def layer_forward(A_prev, W, b, activation):
        '''Implements forward propagation for one layer.

        Args:
            A_prev: Post activation of the previous layer.
            W: weights of the current layer.
            b: biases of the current layer.
            activation: activation of the current layer.
        Returns:
            A: Post activation of the current layer.
            caches: list of caches for back propagation.  
        '''

        Z = np.dot(W, A_prev) + b
        assert(Z.shape == (W.shape[0], A_prev.shape[1]))
        
        A = get_activation(Z, activation)
        assert(A.shape == (W.shape[0], A_prev.shape[1]))
        
        chache = (A_prev, W, b, Z)
        
        return A, chache

    def model_forward(self, X):
        '''Implement forward propagation for the entire network.

        Args:
            X: data as numpy array of size (features, number of examples).
        Returns:
            AL: last post-activation value
            caches: list of caches for back propagation        
        '''
        caches = []
        A = X

        num_layers = len(self.parameters) // 2
        
        
        for l in range(1, num_layers+1):
            A_prev = A
            A, cache = self.layer_forward(A_prev, self.parameters[f'W{l}'], self.parameters[f'b{l}'], activation=self.activations[l-1])
            caches.append(cache)
        
    
        return A, caches

    @staticmethod
    def layer_backward(dA, cache, activation, L2_reg_lambda):
        '''Implements back propagation for one layer.

        Args:
            dA: the derivative of the post activation.
            cache: tuple of values (A_prev, W, b)
            activation: activation of the current layer.
        Returns:
            dA_prev: gradient of the cost with respect to the post activatio of the last layer
            dW: gradient of the cost with respect to the weights of the current layer.
            db: gradient of the cost with respect to the biases of the current layer.
        '''
        A_prev, W, b, Z = cache
        m = A_prev.shape[1]
        
        dZ = activation_backward(dA, Z, activation)
        
        reg_term = 0
        if L2_reg_lambda:
            reg_term = ( 2*L2_reg_lambda / m ) * W
        
        dW = 1/m * np.dot(dZ, A_prev.T) + reg_term
        db = 1/m * np.sum(dZ, axis=1, keepdims=True)
        dA_prev = np.dot(W.T, dZ)
        
        assert(dA_prev.shape == A_prev.shape)
        assert(W.shape == W.shape)
        assert(b.shape == b.shape)
        
        return dA_prev, dW, db


    def model_backward(self, AL, Y, caches):
        '''Implement the backward propagation the entire network.

        Args:
            AL: probability vector of label predictions.
            Y: true labels vector.
            caches: list of caches.
        Returns:
            grads: dictionary with the gradients
        '''
        grads = {}
        num_layers = len(caches)
        m = AL.shape[1]
        
        dAL = grad_cost(AL, Y, self.loss)

        grads[f'dA{num_layers}'] = dAL
        for l in range(num_layers, 0, -1):
            current_cache = caches[l-1]
            grads[f'dA{l-1}'], grads[f'dW{l}'], grads[f'db{l}'] = self.layer_backward(grads[f'dA{l}'], current_cache, self.activations[l-1], self.L2_regularization_lambdas[l-1])
            
        return grads


    @staticmethod
    def iterate_minibatches(X, Y, batchsize, seed=None, shuffle=False):
        '''Splits the data into batches.

        Args:
            X: the features data as numpy array.
            Y: true labels vector.
            batchsize: size of a batch.
            seed: the seed.
            shuffle: shuffles the data if true.
        Returns:
            a generator that yeilds batches as tuple of numpy arrays (features, labels)
        '''
        if not seed:
            np.random.seed(seed)

        assert( X.shape[1] == Y.shape[1] )

        m = X.shape[1]
        num_batches = math.ceil(m/batchsize)
        
        if shuffle:
            permutation = np.random.permutation(X.shape[1])
            shuffled_X = X[:, permutation]
            shuffled_Y = Y[:, permutation].reshape((1,m))
            for k in range(num_batches):
                    mini_batch_X = shuffled_X[:, k*batchsize : (k+1)*batchsize]
                    mini_batch_Y = shuffled_Y[:, k*batchsize : (k+1)*batchsize]
                    yield (mini_batch_X, mini_batch_Y)
        else:
            for k in range(num_batches):
                    mini_batch_X = X[:, k*batchsize : (k+1)*batchsize]
                    mini_batch_Y = Y[:, k*batchsize : (k+1)*batchsize]
                    yield (mini_batch_X, mini_batch_Y)


    def compile(self, optimizer, initializer, loss, metrics):
        '''Configures the model for training(optimizer, initializer, loss function and metrics).

        Args:
            optimizer: optimizer object.
            initializer: initializer object.
            loss: a string of the loss function to use.
            metrics: a string of the metrics function to use.

        The loss functions supported are:
        (binary-cross-entropy, categorical-cross-entropy, mean-squared-error, hinge)
        
        The metrics supported are:
        (accuracy, mean-absolute-error, mean-squared-error, root-mean-square-error, 
        precision, recall, f1-score)
        '''
        self.optimizer = optimizer
        self.initializer = initializer
        self.loss = loss
        self.metrics = metrics

    def fit(self, X, y, batch_size, epochs, shuffle=True, seed=None, print_each_n=50):
        '''Train the model.

        Args:
            X: the features data as numpy array.
            y: true labels vector.
            batchsize: size of a batch.
            epochs: number of iterations over the dataset.
            shuffle: shuffle the data if true.
            seed:
            print_each_n: print the cost each n epoch.
        '''
        m = X.shape[1]  
        self.costs = []
        total_cost = 0

        self.layers_dims[0] = X.shape[0]
        
        self.parameters = self.initializer.initialize_parameters(self.layers_dims)

        self.optimizer.initialize(self.parameters)

        for e in range(epochs):

            for (batch_X, batch_Y) in self.iterate_minibatches(X, y, batch_size, seed, shuffle):

                AL, caches = self.model_forward(batch_X)

                total_cost += ( compute_cost(AL, batch_Y, self.loss) + compute_reg_cost(self.parameters, self.L2_regularization_lambdas) )

                grads = self.model_backward(AL, batch_Y, caches)


                self.parameters = self.optimizer.update_parameters(self.parameters, grads)

            avg_cost = total_cost / (1.*m)
            self.costs.append(avg_cost)

            if e % print_each_n == 0:
                print(f"Epoch {e+1}/{epochs} cost of {avg_cost}")
            total_cost = 0



    def predict(self, X):
        '''Predict the labels for the provided features.

        Args:
            X: the features data as numpy array.
        Returns:
            y_pred: predicted labels.
        '''
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        AL, caches = self.model_forward(X)
        if self.activations[-1] == 'sigmoid':
            y_pred = AL >= 0.5
        elif self.activations[-1] == 'softmax':
            y_pred = np.argmax(AL, axis=0).reshape(1, -1)
        return y_pred


    def evaluate(self, X, y):
        '''Evaluates the network.

        Args:
            X: the features data as numpy array.
            y: true labels vector.
        Returns:
            average cost:
            accuracy:
        '''
        AL, caches = self.model_forward(X)

        if self.activations[-1] == 'sigmoid':
            y_pred = AL >= 0.5
        elif self.activations[-1] == 'softmax':
            y_pred = np.argmax(AL, axis=0).reshape(1, -1)
        acc = compute_score(y, y_pred, 'accuracy')

        # total_cost = compute_cost(AL, y, self.loss)
        total_cost = ( compute_cost(AL, y, self.loss) + compute_reg_cost(self.parameters, self.L2_regularization_lambdas) )

        return total_cost/X.shape[1], acc


    def plot_cost(self):
        '''Draws the cost per epochs.
        '''
        plt.plot(np.squeeze(self.costs))
        plt.ylabel('cost')
        plt.ylim(ymin=0)
        plt.xlabel('iterations')
        plt.xlim(xmin=0)
        plt.title("Learning rate =" + str(self.optimizer.learning_rate))
        plt.show()

    def save(self, file):
        '''Saves the model to a provided file.

        Args:
            file: the file to save the model to.
        '''
        with open(file, "wb") as f:
            pickle.dump(self, f)


def load_model(file):
    '''Loads the model from a provided files.

    Args:
        file: the file to load the model from.
    Returns:
        The model.
    '''
    with open(file, "rb") as f:
        loaded_model = pickle.load(f)
    return loaded_model

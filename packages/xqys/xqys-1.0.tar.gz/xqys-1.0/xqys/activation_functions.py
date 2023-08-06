import numpy as np

def sigmoid(Z):
    A = 1/(1+np.exp(-Z))
    return A

def sigmoid_backward(dA, Z):
    s = 1/(1+np.exp(-Z))
    dZ = dA * s * (1-s)
    
    assert (dZ.shape == Z.shape)
    return dZ

def relu(Z):
    A = np.maximum(0,Z)
    assert(A.shape == Z.shape)
    return A

def relu_backward(dA, Z):
    dZ = np.array(dA, copy=True) 
    
    dZ[Z <= 0] = 0
    assert (dZ.shape == Z.shape)
    return dZ

def softmax(Z):
    exps = np.exp(Z)
    return exps / np.sum(exps, axis=0, keepdims=True)

def softmax_backward(dA, Z):
    return dA

def identity(Z):
    return Z

def identity_backward(dA, Z):
    return dA

def binary_step(Z):
    return Z >= 1

def binary_step_backward(dA, Z):
    # cant be used for learning
    return np.zeros(Z.shape)

def tanh(Z):
    return np.tanh(Z)

def tanh_backward(dA, Z):
    return dA * ( 1 - np.square( np.tanh(Z) ) )

def arctan(Z):
    return np.arctan(Z)

def arctan_backward(dA, Z):
    return dA / (np.square(Z) + 1)

def prelu(Z, alpha=0.01):
    return ( (Z >= 0) * Z ) + ( (Z < 0) * alpha * Z )

def prelu_backward(dA, Z, alpha=0.01):
    return dA * ( (Z >= 0) + (Z < 0) * alpha )

def elu(Z, alpha=0.01):
    return ( (Z >= 0) * Z ) + ( (Z < 0) * alpha * ( np.exp(Z)-1 ) )

def elu_backward(dA, Z, alpha=0.01):
    return dA * ( (Z >= 0) + (Z < 0) * ( alpha + elu(Z, alpha) ) )


def get_activation(Z, name):
    '''Computes the activation of of a specified type.

    Args:
        Z: the input to the activation.
        name: type of the activation to compute.
    Returns:
        the activation of the specified type.
    '''
    if name == 'sigmoid':
        return sigmoid(Z)
    elif name == 'relu':
        return relu(Z)
    elif name == 'softmax':
        return softmax(Z)
    elif name == 'identity':
        return identity(Z)
    elif name == 'binary-step':
        return binary_step(Z)
    elif name == 'tanh':
        return tanh(Z)
    elif name == 'arctan':
        return arctan(Z)
    elif name == 'prelu':
        return prelu(Z)
    elif name == 'elu':
        return elu(Z)



def activation_backward(dA, Z, name):
    '''Computes the derivative of the cost
    with respect to the input of a specified activation.

    Args:
        dA: the derivative of cost with respect to the post activation.
        Z: the input to the activation.
        name: type of the activation.
    Returns:
        the derivative with respect to the activation's input.
    '''
    if name == 'sigmoid':
        return sigmoid_backward(dA, Z)
    elif name == 'relu':
        return relu_backward(dA, Z)
    elif name == 'softmax':
        return softmax_backward(dA, Z)
    elif name == 'identity':
        return identity_backward(dA, Z)
    elif name == 'binary-step':
        return binary_step_backward(dA, Z)
    elif name == 'tanh':
        return tanh_backward(dA, Z)
    elif name == 'arctan':
        return arctan_backward(dA, Z)
    elif name == 'prelu':
        return prelu_backward(dA, Z)
    elif name == 'elu':
        return elu_backward(dA, Z)
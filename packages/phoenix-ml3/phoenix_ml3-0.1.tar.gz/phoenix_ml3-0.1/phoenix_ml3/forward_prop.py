import numpy as np
from .NN import NN as NN


def linear_forward(A, W, b):
    Z = np.dot(W, A) + b
   # assert (Z.shape == (W.shape[0], A.shape[1]))
    cache = (A, W, b)
    return Z, cache


def linear_activation_forward(A_prev, W, b, activation):
    if activation == "sigmoid":
        # Inputs: "A_prev, W, b". Outputs: "A, activation_cache".
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = NN.sigmoid(Z)
    elif activation == "relu":
        # Inputs: "A_prev, W, b". Outputs: "A, activation_cache".
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = NN.relu(Z)
    elif activation == "identity":
        # Inputs: "A_prev, W, b". Outputs: "A, activation_cache".
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = NN.identity(Z)
    elif activation == "tanh":
        # Inputs: "A_prev, W, b". Outputs: "A, activation_cache".
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = NN.tanh(Z)


    #assert (A.shape == (W.shape[0], A_prev.shape[1]))
    cache = (linear_cache, activation_cache)

    return A, cache


def L_model_forward(X, parameters,LayerActivationFunction,A_out):

    caches = []
    A = X
    L = len(parameters) // 2  # number of layers in the neural network

    for l in range(1, L):
        A_prev = A
        A, cache = linear_activation_forward(A_prev, parameters['W' + str(l)], parameters['b' + str(l)],
                                             activation=LayerActivationFunction)
        caches.append(cache)

    output_layer, cache = linear_activation_forward(A, parameters['W' + str(L)], parameters['b' + str(L)], activation=A_out)
    caches.append(cache)

    AL=NN.softmax(output_layer)


    return AL, caches

def compute_cost(AL, Y):


    cost = NN.softmax_loss(AL,Y)

    return cost    
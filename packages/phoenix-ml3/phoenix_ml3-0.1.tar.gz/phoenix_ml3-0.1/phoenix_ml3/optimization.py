import math

import numpy as np
from .init_param import * as init_param
from .forward_prop import * as forward_prop
from .back_prop import * as back_prop
from .visualization import * as visualization



def update_parameters_GD(parameters, grads, learning_rate):

    L = len(parameters) // 2  # number of layers in the neural network

    # Update rule for each parameter. Use a for loop.

    for l in range(L):
        parameters["W" + str(l + 1)] = parameters["W" + str(l + 1)] - (learning_rate * grads["dW" + str(l + 1)])
        parameters["b" + str(l + 1)] = parameters["b" + str(l + 1)] - (learning_rate * grads["db" + str(l + 1)])

    return parameters


"""
layers_dims = row vector of nodes in each layer Ex.[3,2,2,9] inputFeatures = 3 & 3 layers 1st layer = 2.....
Initialization of parameters = ("he","random","zeros")
he intilization is recommended with Relu Activation Function
A_layers = Activation Function of Layers ("relu","sigmoid","identity")
A_out = A_layers = Activation Function of Output Layer ("relu","sigmoid","identity")
"""
def L_layer_model_GD(X, Y, layers_dims,initialization, A_layers , A_out ,prev_parameters = 0,learning_rate=0.0075, num_iterations=1000,  print_cost=True):
    costs = []  # keep track of cost

    # Parameters initialization.
    if initialization == "zeros":
        parameters = init_param.initialize_parameters_zeros(layers_dims)
    elif initialization == "random":
        parameters =init_param.initialize_parameters_random(layers_dims)
    elif initialization == "prev_parameters":
        parameters = prev_parameters



    # Loop (gradient descent)
    for i in range(0, num_iterations):

        # Forward propagation: Activation["relu","sigmoid"]
        AL, caches = forward_prop.L_model_forward(X, parameters,A_layers,A_out)
        # Compute cost.
        cost =  forward_prop.compute_cost(AL, Y)
        # Backward propagation.
        grads = back_prop.L_model_backward(AL, Y, caches,A_layers,A_out)
        # Update parameters.
        parameters = update_parameters_GD(parameters, grads, learning_rate)



        # Print the cost every 100 iteration and i % 100 == 0
        if print_cost and i % 100 == 0:
            print("Cost after iteration %i: %f" % (i, cost))
        if print_cost and i % 100 == 0:
            costs.append(cost)

    # plot the cost
    visualization.draw_costs(costs,learning_rate)


    return parameters




def L_layer_model_SGD(X, Y, layers_dims,initialization, A_layers , A_out ,prev_parameters = 0 ,learning_rate=0.0075, num_iterations=1000,  print_cost=True):


    m = X.shape[1]
    cost = 0
    costs = []
    # Parameters initialization.
    if initialization == "zeros":
        parameters = init_param.initialize_parameters_zeros(layers_dims)
    elif initialization == "random":
        parameters = init_param.initialize_parameters_random(layers_dims)
    elif initialization == "prev_parameters":
        parameters = prev_parameters

    for i in range(0, num_iterations):
        for j in range(0, m):
            # Forward propagation
            input = X[:, j].reshape((X[:, j].shape[0],1))
            a, caches = forward_prop.L_model_forward(input, parameters,A_layers , A_out)
            a = a.reshape(a.shape[0],1)
            # Compute cost
            label = Y[:, j].reshape((Y[:, j].shape[0],1))
            cost += forward_prop.compute_cost(a, label)
            # Backward propagation
            grads = back_prop.L_model_backward(a, label, caches,A_layers,A_out)
            # Update parameters.
            parameters = update_parameters_GD(parameters, grads, learning_rate)

        cost = cost /m

        if print_cost and i % 100 == 0:
            print("Cost after iteration %i: %f" % (i, cost))
        if print_cost and i % 100 == 0:
            costs.append(cost)

        cost = 0

    # plot the cost
    visualization.draw_costs(costs, learning_rate)

    return parameters


def initialize_velocity(parameters):

    L = len(parameters) // 2  # number of layers in the neural networks
    v = {}
    # Initialize velocity
    for l in range(L):
        v["dW" + str(l + 1)] = np.zeros((parameters["W" + str(l + 1)].shape[0], parameters["W" + str(l + 1)].shape[1]))
        v["db" + str(l + 1)] = np.zeros((parameters["b" + str(l + 1)].shape[0], parameters["b" + str(l + 1)].shape[1]))

    return v


def update_parameters_with_momentum(parameters, grads, v, beta, learning_rate):
    """
    Update parameters using Momentum
    """
    L = len(parameters) // 2  # number of layers in the neural networks
    # Momentum update for each parameter
    for l in range(L):
        # compute velocities
        v["dW" + str(l + 1)] = beta * v["dW" + str(l + 1)] + (1 - beta) * grads['dW' + str(l + 1)]
        v["db" + str(l + 1)] = beta * v["db" + str(l + 1)] + (1 - beta) * grads['db' + str(l + 1)]
        # update parameters
        parameters["W" + str(l + 1)] = parameters["W" + str(l + 1)] - learning_rate * v["dW" + str(l + 1)]
        parameters["b" + str(l + 1)] = parameters["b" + str(l + 1)] - learning_rate * v["db" + str(l + 1)]

    return parameters, v


def L_layer_model_GDWithMomentum(X, Y, layers_dims,initialization, A_layers , A_out ,prev_parameters = 0 ,beta=0.9,learning_rate=0.0075, num_iterations=1000,  print_cost=True):


    costs = []  # keep track of cost

    # Parameters initialization.
    if initialization == "zeros":
        parameters = init_param.initialize_parameters_zeros(layers_dims)
    elif initialization == "random":
        parameters =init_param.initialize_parameters_random(layers_dims)
    elif initialization == "prev_parameters":
        parameters = prev_parameters

    # initialize v
    v = initialize_velocity(parameters)

    # Loop (gradient descent)
    for i in range(0, num_iterations):


        # Forward propagation: Activation["relu","sigmoid"]
        AL, caches = forward_prop.L_model_forward(X, parameters,A_layers,A_out)
        # Compute cost.
        cost =  forward_prop.compute_cost(AL, Y)
        # Backward propagation.
        grads = back_prop.L_model_backward(AL, Y, caches,A_layers,A_out)
        # Update parameters.

        parameters , v = update_parameters_with_momentum(parameters, grads, v, beta, learning_rate)



        # Print the cost every 100 iteration and i % 100 == 0
        if print_cost and i % 100 == 0:
            print("Cost after iteration %i: %f" % (i, cost))
        if print_cost and i % 100 == 0:
            costs.append(cost)

    # plot the cost
    visualization.draw_costs(costs,learning_rate)


    return parameters


def initialize_adam(parameters):

    L = len(parameters) // 2  # number of layers in the neural networks
    v = {}
    s = {}
    # Initialize v, s. Input: "parameters". Outputs: "v, s".
    for l in range(L):
        v["dW" + str(l + 1)] = np.zeros((parameters["W" + str(l + 1)].shape[0], parameters["W" + str(l + 1)].shape[1]))
        v["db" + str(l + 1)] = np.zeros((parameters["b" + str(l + 1)].shape[0], parameters["b" + str(l + 1)].shape[1]))
        s["dW" + str(l + 1)] = np.zeros((parameters["W" + str(l + 1)].shape[0], parameters["W" + str(l + 1)].shape[1]))
        s["db" + str(l + 1)] = np.zeros((parameters["b" + str(l + 1)].shape[0], parameters["b" + str(l + 1)].shape[1]))

    return v, s


def update_parameters_with_adam(parameters, grads, v, s, t, learning_rate=0.01,
                                beta1=0.9, beta2=0.999, epsilon=1e-8):

    L = len(parameters) // 2  # number of layers in the neural networks
    v_corrected = {}
    s_corrected = {}

    # Perform Adam update on all parameters
    for l in range(L):

        v["dW" + str(l + 1)] = beta1 * v["dW" + str(l + 1)] + (1 - beta1) * grads['dW' + str(l + 1)]
        v["db" + str(l + 1)] = beta1 * v["db" + str(l + 1)] + (1 - beta1) * grads['db' + str(l + 1)]

        v_corrected["dW" + str(l + 1)] = v["dW" + str(l + 1)] / (1 - beta1 ** t)
        v_corrected["db" + str(l + 1)] = v["db" + str(l + 1)] / (1 - beta1 ** t)
        s["dW" + str(l + 1)] = beta2 * s["dW" + str(l + 1)] + (1 - beta2) * np.square(grads['dW' + str(l + 1)])
        s["db" + str(l + 1)] = beta2 * s["db" + str(l + 1)] + (1 - beta2) * np.square(grads['db' + str(l + 1)])
        s_corrected["dW" + str(l + 1)] = s["dW" + str(l + 1)] / (1 - beta2 ** t)
        s_corrected["db" + str(l + 1)] = s["db" + str(l + 1)] / (1 - beta2 ** t)
        parameters["W" + str(l + 1)] = parameters["W" + str(l + 1)] - learning_rate * v_corrected["dW" + str(l + 1)] / (
                    np.sqrt(s_corrected["dW" + str(l + 1)]) + epsilon)
        parameters["b" + str(l + 1)] = parameters["b" + str(l + 1)] - learning_rate * v_corrected["db" + str(l + 1)] / (
                    np.sqrt(s_corrected["db" + str(l + 1)]) + epsilon)


    return parameters, v, s

def L_layer_model_Adam(X, Y, layers_dims,initialization, A_layers , A_out ,prev_parameters = 0 ,beta1 = 0.9, beta2 = 0.999,  epsilon = 1e-8,learning_rate=0.0075,
                       num_iterations=1000,  print_cost=True):

    costs = []  # keep track of cost

    # Parameters initialization.
    if initialization == "zeros":
        parameters = init_param.initialize_parameters_zeros(layers_dims)
    elif initialization == "random":
        parameters =init_param.initialize_parameters_random(layers_dims)
    elif initialization == "prev_parameters":
        parameters = prev_parameters

    # initialize v ,s
    v ,s = initialize_adam(parameters)

    # Loop (gradient descent)
    for i in range(0, num_iterations):


        # Forward propagation: Activation["relu","sigmoid"]
        AL, caches = forward_prop.L_model_forward(X, parameters,A_layers,A_out)
        # Compute cost.
        cost =  forward_prop.compute_cost(AL, Y)
        # Backward propagation.
        grads = back_prop.L_model_backward(AL, Y, caches,A_layers,A_out)
        # Update parameters.

        parameters , v,s = update_parameters_with_adam(parameters, grads, v, s, i+1, learning_rate,
                                beta1, beta2, epsilon)



        # Print the cost every 100 iteration and i % 100 == 0
        if print_cost and i % 100 == 0:
            print("Cost after iteration %i: %f" % (i, cost))
        if print_cost and i % 100 == 0:
            costs.append(cost)

    # plot the cost
    visualization.draw_costs(costs,learning_rate)


    return parameters


def random_mini_batches(X, Y, mini_batch_size=64):


    m = X.shape[1]  # number of training examples
    mini_batches = []


    # Shuffle (X, Y)
    permutation = list(np.random.permutation(m))
    shuffled_X = X[:, permutation]
    shuffled_Y = Y[:, permutation]
    num_complete_minibatches = math.floor( m / mini_batch_size)  # number of mini batches of size mini_batch_size

    for k in range(0, num_complete_minibatches):
        mini_batch_X = shuffled_X[:, k * mini_batch_size: (k + 1) * mini_batch_size]
        mini_batch_Y = shuffled_Y[:, k * mini_batch_size: (k + 1) * mini_batch_size]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    # Handling the end case (last mini-batch < mini_batch_size)
    if m % mini_batch_size != 0:
        mini_batch_X = shuffled_X[:, num_complete_minibatches * mini_batch_size:]
        mini_batch_Y = shuffled_Y[:, num_complete_minibatches * mini_batch_size:]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    return mini_batches


def L_layer_model_minibatch(X, Y, layers_dims, optimizer,initialization, A_layers , A_out,prev_parameters = 0, mini_batch_size=64,learning_rate=0.0007, beta=0.9,
          beta1=0.9, beta2=0.999, epsilon=1e-8, num_iterations=1000, print_cost=True):


    L = len(layers_dims)  # number of layers in the neural networks
    costs = []  # to keep track of the cost
    t = 0  # initializing the counter required for Adam update
    m = X.shape[1]  # number of training examples

    # Parameters initialization.
    if initialization == "zeros":
        parameters = init_param.initialize_parameters_zeros(layers_dims)
    elif initialization == "random":
        parameters = init_param.initialize_parameters_random(layers_dims)
    elif initialization == "prev_parameters":
        parameters = prev_parameters

    # Initialize the optimizer
    if optimizer == "gd":
        pass  # no initialization required for gradient descent
    elif optimizer == "momentum":
        v = initialize_velocity(parameters)
    elif optimizer == "adam":
        v, s = initialize_adam(parameters)

    # Optimization loop
    for i in range(num_iterations):


        minibatches = random_mini_batches(X, Y, mini_batch_size)
        cost_total = 0

        for minibatch in minibatches:

            # Select a minibatch
            (minibatch_X, minibatch_Y) = minibatch

            # Forward propagation
            AL, caches = forward_prop.L_model_forward(minibatch_X, parameters,A_layers,A_out)

            # Compute cost and add to the cost total
            cost_total += forward_prop.compute_cost(AL,minibatch_Y)*mini_batch_size

            # Backward propagation
            grads = back_prop.L_model_backward(AL, minibatch_Y, caches,A_layers,A_out)

            # Update parameters
            if optimizer == "gd":
                parameters = update_parameters_GD(parameters, grads, learning_rate)
            elif optimizer == "momentum":
                parameters, v = update_parameters_with_momentum(parameters, grads, v, beta, learning_rate)
            elif optimizer == "adam":
                t = t + 1  # Adam counter
                parameters, v, s = update_parameters_with_adam(parameters, grads, v, s, t, learning_rate,beta1, beta2, epsilon)
        cost_avg = cost_total / m

        # Print the cost every 1000 iteration
        if print_cost and i % 100 == 0:
            print("Cost after iteration %i: %f" % (i, cost_avg))
        if print_cost and i % 100 == 0:
            costs.append(cost_avg)

    # plot the cost
    visualization.draw_costs(costs, learning_rate)


    return parameters
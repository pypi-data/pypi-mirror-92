import numpy as np
import math
import matplotlib.pyplot as plt
import pickle
from urllib import request
import gzip
import pandas as pd
import seaborn as sn
from prettytable import PrettyTable
from IPython.display import display

def save_parameters(filename,parameters):
    open_file = open(filename, "wb")
    pickle.dump(parameters, open_file)
    open_file.close()

def load_parameters(filename):
    open_file = open(filename, "rb")
    loaded_parameters = pickle.load(open_file)
    open_file.close()
    return loaded_parameters
def download_mnist():
    filename = [
        ["training_images", "train-images-idx3-ubyte.gz"],
        ["test_images", "t10k-images-idx3-ubyte.gz"],
        ["training_labels", "train-labels-idx1-ubyte.gz"],
        ["test_labels", "t10k-labels-idx1-ubyte.gz"]]
    base_url = "http://yann.lecun.com/exdb/mnist/"
    for name in filename:
        print("Downloading " + name[1] + "...")
        request.urlretrieve(base_url + name[1], name[1])
    print("Download complete.")


def save_mnist():
    filename = [
        ["training_images", "train-images-idx3-ubyte.gz"],
        ["test_images", "t10k-images-idx3-ubyte.gz"],
        ["training_labels", "train-labels-idx1-ubyte.gz"],
        ["test_labels", "t10k-labels-idx1-ubyte.gz"]]
    mnist = {}
    for name in filename[:2]:
        with gzip.open(name[1], 'rb') as f:
            mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1, 28 * 28)
    for name in filename[-2:]:
        with gzip.open(name[1], 'rb') as f:
            mnist[name[0]] = np.frombuffer(f.read(), np.uint8, offset=8)
    with open("mnist.pkl", 'wb') as f:
        pickle.dump(mnist, f)
    print("Save complete.")


def load():
    with open("mnist.pkl", 'rb') as f:
        mnist = pickle.load(f)
    return mnist["training_images"], mnist["training_labels"], mnist["test_images"], mnist["test_labels"]


def MakeOneHot(Y, D_out):
    N = Y.shape[0]
    Z = np.zeros((N, D_out))
    Z[np.arange(N), Y] = 1
    return Z

def initialize_parameters_zeros(layers_dims):

    parameters = {}
    L = len(layers_dims)  # number of layers in the network

    for l in range(1, L):
        parameters['W' + str(l)] = np.zeros((layers_dims[l], layers_dims[l - 1]))
        parameters['b' + str(l)] = np.zeros((layers_dims[l], 1))

        assert (parameters['W' + str(l)].shape == (layers_dims[l], layers_dims[l - 1]))
        assert (parameters['b' + str(l)].shape == (layers_dims[l], 1))
    return parameters


def initialize_parameters_random(layers_dims):
    parameters = {}
    L = len(layers_dims)  # integer representing the number of layers
    for l in range(1, L):
        parameters['W' + str(l)] = np.random.randn(layers_dims[l], layers_dims[l - 1]) * 0.01
        parameters['b' + str(l)] = np.zeros((layers_dims[l], 1))

    return parameters



def identity(z):

    s = z
    cache = z
    return s , cache

def identity_derivative(dout, z):
    dz = dout * 1

    return dz

def sigmoid(z):
    s = 1 / (1 + np.exp(-z))
    cache = z

    return s , cache


def sigmoid_derivative(dout, cache):
    z = cache
    A , temp = sigmoid(z)
    dz = dout * A * (1 - A)
    return dz


def relu(z):
    a = np.maximum(0, z)
    cache = z
    return a , cache


def relu_backward(dout, cache):
    z = cache
    dz = np.array(dout, copy=True)  # just converting dz to a correct object.
    # When z <= 0, you should set dz to 0 as well.
    dz[z <= 0] = 0
    return dz


def tanh(z):
    z = np.tanh(z)
    cache = z

    return z , cache


def tanh_derivative(dout, z):

    dz = dout * (1 - np.tanh(z) ** 2)

    return dz


def compute_cost(Y_pred, Y, loss_name):
    if loss_name == "L1":
        loss = np.sum(np.abs(Y - Y_pred))
    # linear regression-squareloss-linear activation function-L2
    if loss_name == "square_loss":
        loss = np.dot(Y - Y_pred, Y - Y_pred)
    # smooth loss function , linear activation
    if loss_name == "smooth_loss":
        loss = np.max(0.0, -Y_pred)
    # logistic regression -Loglikelihood loss function , linear activation function
    if loss_name == "Logistic_regression_alternative":
        loss = np.log(1 + np.exp(np.dot(-Y, Y_pred)))
    # logistic regression -Loglikelihood loss function -sigmoid activation function
    if loss_name == "logistic_regression_loss":
        loss = -np.log(np.sum((Y / 2) * 0.5), Y_pred)

    # hinge loss for SVM , using linear activation function
    if loss_name == "hingeloss":
        loss = np.max([0.0, 1 - Y_pred * Y])
    return loss


def softmax(Zout):
    #  Z is vector of dim(1,classesNo.)
    Z = np.exp(Zout)
    sum = Z.sum(axis=0)
    probabilities = (1 / sum) * Z
    return probabilities

def softmax_loss(Y_pred, Y_true):
    """
    Negative log likelihood loss
    """
    loss = 0.0

    M = Y_pred.shape[1]
    y_r = np.sum( (Y_pred*Y_true) , axis=0)
    for e in y_r:
        if e == 0:
            loss += 500
        else:
            loss += -np.log(e)


    return loss/M

def linear_forward(A, W, b):
    Z = np.dot(W, A) + b
   # assert (Z.shape == (W.shape[0], A.shape[1]))
    cache = (A, W, b)
    return Z, cache


def linear_activation_forward(A_prev, W, b, activation):
    if activation == "sigmoid":
        # Inputs: "A_prev, W, b". Outputs: "A, activation_cache".
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = sigmoid(Z)
    elif activation == "relu":
        # Inputs: "A_prev, W, b". Outputs: "A, activation_cache".
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = relu(Z)
    elif activation == "identity":
        # Inputs: "A_prev, W, b". Outputs: "A, activation_cache".
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = identity(Z)
    elif activation == "tanh":
        # Inputs: "A_prev, W, b". Outputs: "A, activation_cache".
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = tanh(Z)


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

    AL=softmax(output_layer)


    return AL, caches

def compute_cost(AL, Y):


    cost = softmax_loss(AL,Y)

    return cost

def draw_costs(costs,learning_rate):
    plt.plot(np.squeeze(costs))
    plt.ylabel('cost')
    plt.xlabel('iterations')
    plt.title("Learning rate =" + str(learning_rate))
    plt.show()

def linear_backward(dZ, cache): #dl/dw
    A_prev, W, b = cache
    m = A_prev.shape[1]

    dW = 1 / m * np.dot(dZ, A_prev.T)
    db = 1 / m * np.sum(dZ, axis=1, keepdims=True)
    dA_prev = np.dot(W.T, dZ)

    assert (dA_prev.shape == A_prev.shape)
    assert (dW.shape == W.shape)
    assert (db.shape == b.shape)

    return dA_prev, dW, db


def linear_activation_backward(dA, cache, activation): #dl/dz

    linear_cache, activation_cache = cache

    if activation == "relu":
        dZ = relu_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)

    elif activation == "sigmoid":
        dZ = sigmoid_derivative(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)

    elif activation == "identity":
        dZ = identity_derivative(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)

    elif activation == "tanh":
        dZ = tanh_derivative(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)

    return dA_prev, dW, db


def L_model_backward(AL, Y, caches,LayerActivationFunction,A_out):

    grads = {}
    L = len(caches)  # the number of layers
    m = AL.shape[1]
    Y = Y.reshape(AL.shape)  # after this line, Y is the same shape as AL
    # Initializing the backpropagation
    # derivative of cost with respect to AL
    N = AL.shape[1]
    Y_serial = np.argmax(Y, axis=0)
    dAL = AL.copy()
    dAL[Y_serial, np.arange(N)] -= 1
    current_cache = caches[L - 1]
    grads["dA" + str(L - 1)], grads["dW" + str(L)], grads["db" + str(L)] = linear_activation_backward(dAL,current_cache,A_out)
    # Loop from l=L-2 to l=0
    for l in reversed(range(L - 1)):
        # lth layer: (RELU -> LINEAR) gradients.
        # Inputs: "grads["dA" + str(l + 1)], current_cache". Outputs: "grads["dA" + str(l)] , grads["dW" + str(l + 1)] , grads["db" + str(l + 1)]
        current_cache = caches[l]
        dA_prev_temp, dW_temp, db_temp = linear_activation_backward(grads["dA" + str(l + 1)], current_cache, LayerActivationFunction)
        grads["dA" + str(l)] = dA_prev_temp
        grads["dW" + str(l + 1)] = dW_temp
        grads["db" + str(l + 1)] = db_temp

    return grads


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
def L_layer_model_GD(X, Y, layers_dims,initialization, A_layers , A_out ,prev_parameters = 0,learning_rate=0.0075, num_iterations=1000,  print_cost=True,print_every=100):
    costs = []  # keep track of cost

    # Parameters initialization.
    if initialization == "zeros":
        parameters = initialize_parameters_zeros(layers_dims)
    elif initialization == "random":
        parameters =initialize_parameters_random(layers_dims)
    elif initialization == "prev_parameters":
        parameters = prev_parameters



    # Loop (gradient descent)
    for i in range(0, num_iterations):

        # Forward propagation: Activation["relu","sigmoid"]
        AL, caches = L_model_forward(X, parameters,A_layers,A_out)
        # Compute cost.
        cost =  compute_cost(AL, Y)
        # Backward propagation.
        grads = L_model_backward(AL, Y, caches,A_layers,A_out)
        # Update parameters.
        parameters = update_parameters_GD(parameters, grads, learning_rate)

        # Print the cost every 100 iteration and i % 100 == 0
        if print_cost and i % print_every == 0:
            print("Cost after iteration %i: %f" % (i, cost))
        if print_cost and i % print_every == 0:
            costs.append(cost)

    # plot the cost
    draw_costs(costs,learning_rate)


    return parameters




def L_layer_model_SGD(X, Y, layers_dims,initialization, A_layers , A_out ,prev_parameters = 0 ,learning_rate=0.0075, num_iterations=1000,  print_cost=True,print_every=100):


    m = X.shape[1]
    cost = 0
    costs = []
    # Parameters initialization.
    if initialization == "zeros":
        parameters = initialize_parameters_zeros(layers_dims)
    elif initialization == "random":
        parameters = initialize_parameters_random(layers_dims)
    elif initialization == "prev_parameters":
        parameters = prev_parameters

    for i in range(0, num_iterations):
        for j in range(0, m):
            # Forward propagation
            input = X[:, j].reshape((X[:, j].shape[0],1))
            a, caches = L_model_forward(input, parameters,A_layers , A_out)
            a = a.reshape(a.shape[0],1)
            # Compute cost
            label = Y[:, j].reshape((Y[:, j].shape[0],1))
            cost += compute_cost(a, label)
            # Backward propagation
            grads = L_model_backward(a, label, caches,A_layers,A_out)
            # Update parameters.
            parameters = update_parameters_GD(parameters, grads, learning_rate)

        cost = cost /m

        # Print the cost every 100 iteration and i % 100 == 0
        if print_cost and i % print_every == 0:
            print("Cost after iteration %i: %f" % (i, cost))
        if print_cost and i % print_every == 0:
            costs.append(cost)

        cost = 0

    # plot the cost
    draw_costs(costs, learning_rate)

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


def L_layer_model_GDWithMomentum(X, Y, layers_dims,initialization, A_layers , A_out ,prev_parameters = 0 ,beta=0.9,learning_rate=0.0075, num_iterations=1000,  print_cost=True,print_every=100):


    costs = []  # keep track of cost

    # Parameters initialization.
    if initialization == "zeros":
        parameters = initialize_parameters_zeros(layers_dims)
    elif initialization == "random":
        parameters =initialize_parameters_random(layers_dims)
    elif initialization == "prev_parameters":
        parameters = prev_parameters

    # initialize v
    v = initialize_velocity(parameters)

    # Loop (gradient descent)
    for i in range(0, num_iterations):


        # Forward propagation: Activation["relu","sigmoid"]
        AL, caches = L_model_forward(X, parameters,A_layers,A_out)
        # Compute cost.
        cost = compute_cost(AL, Y)
        # Backward propagation.
        grads = L_model_backward(AL, Y, caches,A_layers,A_out)
        # Update parameters.

        parameters , v = update_parameters_with_momentum(parameters, grads, v, beta, learning_rate)

        # Print the cost every 100 iteration and i % 100 == 0
        if print_cost and i % print_every == 0:
            print("Cost after iteration %i: %f" % (i, cost))
        if print_cost and i % print_every == 0:
            costs.append(cost)

    # plot the cost
    draw_costs(costs,learning_rate)


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
                       num_iterations=1000,  print_cost=True,print_every=100):

    costs = []  # keep track of cost

    # Parameters initialization.
    if initialization == "zeros":
        parameters = initialize_parameters_zeros(layers_dims)
    elif initialization == "random":
        parameters =initialize_parameters_random(layers_dims)
    elif initialization == "prev_parameters":
        parameters = prev_parameters

    # initialize v ,s
    v ,s = initialize_adam(parameters)

    # Loop (gradient descent)
    for i in range(0, num_iterations):


        # Forward propagation: Activation["relu","sigmoid"]
        AL, caches = L_model_forward(X, parameters,A_layers,A_out)
        # Compute cost.
        cost =  compute_cost(AL, Y)
        # Backward propagation.
        grads = L_model_backward(AL, Y, caches,A_layers,A_out)
        # Update parameters.

        parameters , v,s = update_parameters_with_adam(parameters, grads, v, s, i+1, learning_rate,
                                beta1, beta2, epsilon)



        # Print the cost every 100 iteration and i % 100 == 0

        # Print the cost every 100 iteration and i % 100 == 0
        if print_cost and i % print_every == 0:
            print("Cost after iteration %i: %f" % (i, cost))
        if print_cost and i % print_every == 0:
            costs.append(cost)

    # plot the cost
    draw_costs(costs,learning_rate)


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
          beta1=0.9, beta2=0.999, epsilon=1e-8, num_iterations=1000, print_cost=True,print_every=100):


    L = len(layers_dims)  # number of layers in the neural networks
    costs = []  # to keep track of the cost
    t = 0  # initializing the counter required for Adam update
    m = X.shape[1]  # number of training examples

    # Parameters initialization.
    if initialization == "zeros":
        parameters = initialize_parameters_zeros(layers_dims)
    elif initialization == "random":
        parameters = initialize_parameters_random(layers_dims)
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
            AL, caches = L_model_forward(minibatch_X, parameters,A_layers,A_out)

            # Compute cost and add to the cost total
            cost_total += compute_cost(AL,minibatch_Y)*mini_batch_size

            # Backward propagation
            grads = L_model_backward(AL, minibatch_Y, caches,A_layers,A_out)

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

        # Print the cost every 100 iteration and i % 100 == 0
        if print_cost and i % print_every == 0:
            print("Cost after iteration %i: %f" % (i, cost_avg))
        if print_cost and i % print_every == 0:
            costs.append(cost_avg)

    # plot the cost
    draw_costs(costs, learning_rate)


    return parameters

def confusionmatrix(currentDataClass, predictedClass):
    classes = set(currentDataClass)
    number_of_classes = len(classes)
    conf_matrix = pd.DataFrame(np.zeros((number_of_classes, number_of_classes),dtype=int), index=classes, columns=classes)
    for i, j in zip(currentDataClass,predictedClass):
        conf_matrix.loc[i, j] += 1
    fp = conf_matrix.sum(axis=0) - np.diag(conf_matrix)
    fn = conf_matrix.sum(axis=1) - np.diag(conf_matrix)
    tp = np.diag(conf_matrix)
    tn = conf_matrix.values.sum() - (fp + fn + tp)
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    accuracy[np.isnan(accuracy)] = 0.0
    precision = tp / (tp + fp)
    precision[np.isnan(precision)] = 0.0
    recall = tp / (tp + fn)
    recall[np.isnan(recall)] = 0.0
    f1score = (2 * tp) / ((2 * tp) + fp + fn)
    f1score[np.isnan(f1score)] = 0.0
    plt.figure(figsize=(10,7))
    sn.set(font_scale=1.4) # for label size
    sn.heatmap(conf_matrix, annot=True, annot_kws={"size": 16}) # font size
    plt.xlabel('Predicted', size=20);
    plt.ylabel('Target', size=20)
    plt.title('Confusion Matrix', fontsize=18)
    plt.show()
    print(conf_matrix.values)
    x = PrettyTable()
    x.field_names = ["FP", "FN", "TP", "TN", "Accuracy", "Precision", "Recall", "F1 score"]
    x.add_row([fp, fn, np.diagflat(tp), tn, accuracy, precision, recall, f1score])
    print(x)


def drop_missing(dataset, threshold=0.45, drop_cols=[]):
    """
    Process missing columns

  Returns
    ----------
    Dataset with the columns dropped
    Dropped columns name as a list

  Parameters
    ----------
    dataset : DataSet


    threshold : default=0.45
    amount of missing value in columns required to drop the column

    drop_cols : default=[]
    list of columns to be dropped. If not given, function will drop column based on amount of missing values

    """

    if not drop_cols:
        rows = len(dataset)
        num_of_nones = round((1 - threshold) * rows, 0)
        for k, v in (dataset.isnull().sum() / rows).items():  # for loop for appending the keys of dropped columns
            if v > threshold:
                drop_cols.append(k)

        d = dataset.dropna(axis=1,
                           thresh=num_of_nones)  # axis = 1 : remove coloumn , thresh : no. of nons to ramove column
    else:
        d = dataset.drop(drop_cols, axis=1)

    return d, drop_cols


def fill_numeric(dataset, missing_val):
    """
 Helper function that replace NAs numeric values with the median of the column

     Returns
        ----------
        missing_val with columns as key and median of the respective column as values

      Parameters
        ----------
        dataset :  Dataset
        missing_val: Dictionary with column name as key and nan values

    """
    for col in dataset.columns:
        if pd.api.types.is_numeric_dtype(dataset[col].dtypes):
            if dataset[col].isnull().sum():
                dataset[col].fillna(dataset[col].median(), inplace=True)
                missing_val[col] = dataset[col].median()
    return missing_val


def process_missing(dataset, missing_val={}):
    """
 Process missing values


    Returns
    ----------
      Dataset with missing values filled
      missing_val with columns as key and median of the respective column as values

    Parameters
    ----------
      dataset : DataSet
      missing_val : default={}
      Dictionary with column names as keys, value to replace NAs as values. If not given, function will replace numeric missing
      values with median of the respective column

    """
    d = dataset.copy()
    if not missing_val:
        missing_val = fill_numeric(d, missing_val)

    else:
        for k, v in missing_val.items():
            if d[k].isnull().sum():
                d[k].fillna(v, inplace=True)

        if d.isnull().sum().sum():
            for col in d.columns:
                missing_val = fill_numeric(d, missing_val)

    return d, missing_val


def convert_cat(dataset, category_cols=[]):
    """
    Helper method to convert column type to category

    :param dataset: Dateset
    :param category_cols: list of categorical columns needed to be encoded by default loop all
    :return: dataset and dictionary of cols which is category type
    """
    if category_cols:
        for col in category_cols:
            dataset[col] = dataset[col].astype("category")
    else:
        obj_columns = dataset.select_dtypes(['object']).columns
        for obj in obj_columns:
            dataset[obj] = dataset[obj].astype('category')
            category_cols.append(obj)
    return dataset, category_cols


def set_cat(dataset, cat_dict={}):
    """
Helper method to convert column type to category

    :param dataset: Dataset
    :param cat_dict: dictionary of categorical columns: list of cols needed to encoded as categories. by default loop
    all columns
    :return: dictionary of categorical columns
    """
    if cat_dict:
        for k, v in cat_dict.items():
            dataset[k] = dataset[k].cat.set_categories(v)
    else:
        for col in dataset.columns:
            if dataset[col].dtypes.name == "category":
                cat_dict[col] = dataset[col].cat.categories
    return cat_dict


def gen_dummies(dataset, cat_cols, max_cardi):
    """
    Helper method to Convert categorical variable into dummy/indicator variables.


    :param dataset: Dataset
    :param cat_cols: list of categorical columns
    :param max_cardi: max number of categories in column
    :return: dataset and list of cardinality clumns
    """
    cardi_cols = []
    for col in cat_cols:
        if len(dataset[col].cat.categories) <= max_cardi:
            cardi_cols.append(col)

    dataset = pd.get_dummies(dataset, columns=cardi_cols, prefix=cardi_cols, drop_first=True)

    return dataset, cardi_cols


def cat_codes(dataset, cat_cols):
    """
Helper method to encode categories
    :param dataset: Dataset
    :param cat_cols:list of categorical columns (categorical features)
    :return: none
    """
    for col in cat_cols:
        dataset[col] = dataset[col].cat.codes + 1  # series of codes from 1 to max cardinality


def process_cat(dataset, cat_cols=[], cat_dict={}, max_cardi=None):
    """
    Process categorical variables

    Returns
    ----------
    Dataset with categorical variables processed
    cat_dict with categorical columns as key and respective pandas.Series.cat.categories as values

    Parameters
    ----------
    dataset: Dataset

    cat_cols : default=[]
    list of pre-determined categorical variables

    cat_dict : default={}
    Dict with categorical variables as keys and pandas.Series.cat.categories as values. If not given, cat_dict is
    generated with for every categorical columns

    max_cardi : default=None
    maximum cardinality of the categorical variables. Which is the number of class in the categorical features.
    Categories variables with cardinality less or equal to max_cardi will be onehotencoded to produce dummies variables
    """
    d = dataset.copy()

    d, cat_cols = convert_cat(d, cat_cols)

    cat_dict = set_cat(d, cat_dict)

    if max_cardi:
        d, cardi_cols = gen_dummies(d, cat_cols, max_cardi)
        cat_cols = list(set(cat_cols) - set(cardi_cols))

    cat_codes(d, cat_cols)

    return d, cat_dict


def train_valid_split(dataset, num_valid, shuffle=False):
    """
    Split dataset into training and validation set

    Returns
    ----------
    Training and validation set respectively

    Parameters
    ----------
      dataset : Dataset

      num_valid : number of samples needed in validation set

    shuffle : default=False
    Shuffle the rows to randomly sample training and validation sets

    """
    if shuffle:
        dataset = dataset.sample(frac=1).reset_index(drop=True)

    n_trn = len(dataset) - num_valid
    n_train = dataset[:n_trn]
    n_valid = dataset[n_trn:]

    return n_train, n_valid


def display_all(dataset):
    """
    display all data
    Set max rows and columns to display
    Return: None
    """
    with pd.option_context("display.max_rows", 1200):
        with pd.option_context("display.max_columns", 1200):
            display(dataset)


def zero_pad(X, pad):
    X_pad = np.pad(X, ((0, 0), (pad, pad), (pad, pad), (0, 0)), mode='constant', constant_values=(0, 0))
    return X_pad


def conv_single_step(a_slice_prev, W, b):
    s = np.multiply(a_slice_prev, W)
    Z = np.sum(s)
    Z = Z + float(b)
    return Z


def conv(A_prev, W, b, stride, pad):
    (m, n_H_prev, n_W_prev, n_C_prev) = A_prev.shape[0], A_prev.shape[1], A_prev.shape[2], A_prev.shape[3]
    (f, f, n_C_prev, n_C) = W.shape[0], W.shape[1], W.shape[2], W.shape[3]
    n_H = int(int(n_H_prev + 2 * pad - f) / stride + 1)
    n_W = int(int(n_W_prev + 2 * pad - f) / stride + 1)
    Z = np.zeros([m, n_H, n_W, n_C])
    A_prev_pad = zero_pad(A_prev, pad)

    for i in range(m):
        a_prev_pad = A_prev_pad[i]
        for h in range(n_H):
            vert_start = stride * h
            vert_end = vert_start + f

            for w in range(n_W):

                horiz_start = stride * w
                horiz_end = horiz_start + f

                for c in range(n_C):
                    a_slice_prev = A_prev_pad[i, vert_start:vert_end, horiz_start:horiz_end, :]

                    weights = W[:, :, :, c]
                    biases = b[:, :, :, c]
                    Z[i, h, w, c] = conv_single_step(a_slice_prev, weights, biases)

    assert (Z.shape == (m, n_H, n_W, n_C))

    return Z


def pool(A_prev, f, stride, mode="max"):
    (m, n_H_prev, n_W_prev, n_C_prev) = A_prev.shape

    n_H = int(1 + (n_H_prev - f) / stride)
    n_W = int(1 + (n_W_prev - f) / stride)
    n_C = n_C_prev

    A = np.zeros((m, n_H, n_W, n_C))

    for i in range(m):
        for h in range(n_H):
            vert_start = stride * h
            vert_end = vert_start + f

            for w in range(n_W):
                horiz_start = stride * w
                horiz_end = horiz_start + f

                for c in range(n_C):

                    a_prev_slice = A_prev[i]

                    if mode == "max":
                        A[i, h, w, c] = np.max(a_prev_slice[vert_start:vert_end, horiz_start:horiz_end, c])
                    elif mode == "average":
                        A[i, h, w, c] = np.mean(a_prev_slice[vert_start:vert_end, horiz_start:horiz_end, c])

    return A
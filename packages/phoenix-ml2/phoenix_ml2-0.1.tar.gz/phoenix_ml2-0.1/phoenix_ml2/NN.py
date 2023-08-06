import numpy as np

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
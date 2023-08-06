import numpy as np


def sigmoid(z):
    """ This function applies sigmoid function(has mathematical form) as an activation function of a node for forwardpropagation.

    Parameters:

        z (numpy array): result of W.X (Weights.Inputs/features).

    Returns:

        (numpy array): Returning array of same size as input "z" after applying sigmoid on input.
   """
    s = 1 / (1 + np.exp(-z))
    return s


def sigmoid_der(A):
    """ This function applies sigmoid derivative function(has mathematical form) for backpropagation.

    Parameters:

        A (numpy array): result of W.X (Weights.Inputs/features).

    Returns:

        (numpy array): Returning array of same size as input "A".
   """
    return A * (1 - A)


def identity(z):
    """ This function applies identity function(has no mathematical form) as an activation function of a node for forwardpropagation.

    Parameters:

        z (numpy array): result of W.X (Weights.Inputs/features).

    Returns:

        (numpy array): Returning same array of input "z".
   """
    return z


def identity_der(z):
    """ This function applies identity derivative function(has no mathematical form) for backpropagation.

    Parameters:

        z (numpy array): result of W.X (Weights.Inputs/features).

    Returns:

        (int): Returning 1 as its derivative of z.
   """
    return 1


def tanh(z):
    """ This function applies tanh function(has mathematical form) as an activation function of a node for forwardpropagation.

    Parameters:

        z (numpy array): result of W.X (Weights.Inputs/features).

    Returns:

        (numpy array): Returning array of same size as input "z" after applying "tanh()".
   """
    return np.tanh(z)


def tanh_der(A):
    """ This function applies tanh derivative function(has mathematical form) for backpropagation.

    Parameters:

        A (numpy array): result of W.X (Weights.Inputs/features).

    Returns:

        (numpy array): Returning array of same size as input "A" after applying derivative of tanh().
   """
    return 1 - A ** 2


# added in colab
def softmax(z):
    """ This function applies softmax function(has mathematical form) as an activation function of a node for forwardpropagation.

    Parameters:

        z (numpy array): result of W.X (Weights.Inputs/features).

    Returns:

        (numpy array): Returning array of same size as input "z" after applying "exp()/sum of exponential of all inputs".
   """

    # print("in softmax")
    return np.exp(z) / (np.exp(z).sum(axis=0))


# added in colab
def softmax_der(A):
    """ This function applies softmax derivative function(has mathematical form = 1) for backpropagation.

    Parameters:

        A (numpy array): result of W.X (Weights.Inputs/features).

    Returns:

        (int): Returning 1.
   """

    # print("in softmax der")
    # temporaryly
    return 1


def relu(z):
    """ This function applies relu function(has mathematical form) as an activation function of a node for forwardpropagation.

    Parameters:

        z (numpy array): result of W.X (Weights.Inputs/features).

    Returns:

        (numpy array): Returning array of same size as input "z" after applying "max(0,input)".
   """

    A = np.maximum(0, z)
    return A


def relu_der(A):
    """ This function applies relu derivative function(has mathematical form = 1) for backpropagation

    Parameters:

        A (numpy array): result of W.X (Weights.Inputs/features)

    Returns:

        (numpy array): Returning array of same size as input "A", has 2 conditions; if less than zero then 0, else 1.
   """

    Z = np.array(A, copy=True)
    der = np.array(A, copy=True)

    der[Z <= 0] = 0
    der[Z > 0] = 1

    return der


def determine_der_act_func(func):
    """ This function works as a switch, returns the right dervative function for backpropagation as an opposite operation of applied activation function in forwardpropagation.

    Parameters:

        func (method): The activation function used in forwardpropagation.

    Returns:

        (method): Returning method of selective derivative activation function to make backpropagation
   """
    if func == sigmoid:
        return sigmoid_der
    elif func == tanh:
        return tanh_der
    elif func == relu:
        return relu_der
    elif func == softmax:
        return softmax_der
    elif func == identity:
        return identity_der


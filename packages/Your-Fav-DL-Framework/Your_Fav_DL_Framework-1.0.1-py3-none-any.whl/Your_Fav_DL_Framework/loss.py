import numpy as np


def cross_entropy(m, A, Y):  # Log LikelihoodLoss Function - Logistic Regression Sigmoid Activation Function
    """Log LikelihoodLoss Function - Logistic Regression Sigmoid Activation Function

    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
        cost(float): the total loss
    """
    cost = (- 1 / m) * np.sum(Y * np.log(A) + (1 - Y) * (np.log(1 - A)))  # compute cost
    return cost


def cross_entropy_der(m, A, Y):
    """The Derivative of Log LikelihoodLoss Function
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
        (Array of floats): The derivative values of cost function
    """
    return ((-1 * Y) / A) + ((1 - Y) / (1 - A))


def perceptron_criteria(m, A, Y):
    """Perceptron Criteria

    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
        cost(float): the total loss
    """


    cost = (1 / m) * np.sum(np.maximum(0, - Y * A))
    return cost


def perceptron_criteria_der(m, A, Y):
    """The Derivative of Perceptron Criteria loss Function
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
        b(Array of floats): The derivative values of cost function
    """
    A.reshape(m)
    Y.reshape(m)
    p = Y * A
    b = np.zeros(A.shape)
    b[p > 0] = 0
    b[p <= 0] = -Y[p <= 0]
    b[b == 0] = -1
    return b  # .reshape(1,m)


def svm(m, A, Y):
    """Hinge Loss (Soft Margin) SVM

    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
        cost(float): the total loss
    """
    cost = (1 / m) * np.sum(np.maximum(0, 1 - Y * A))
    return cost


def svm_der(m, A, Y):
    """The Derivative of Hinge Loss (Soft Margin) SVM Function
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
        b(Array of floats): The derivative values of cost function
    """
    A.reshape(m)
    Y.reshape(m)
    p = Y * A - 1
    b = np.zeros(A.shape)
    b[p > 0] = 0
    b[p <= 0] = -Y[p <= 0]
    b[b == 0] = -1
    return b  # .reshape(1,m)





def cross_multi_class(m, A,
                      Y):  # Multiclass Log LikelihoodLoss Function - Logistic Regression SoftMax Activation Function
    # v1 = Y * A
    # v2 = np.max(v1,axis=0)
    # v3 = np.log(v2).sum()
    # return (-1 / m) * v3
    """Multiclass Log LikelihoodLoss Function - Logistic Regression SoftMax Activation Function
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
        cost(float): the total loss
    """
    cost = (-1 / m) * np.sum((Y) * (np.log(A)))
    # print("in cross multi")
    return cost


def cross_multi_class_der(m, A, Y):
    """The Derivative of Multiclass Log LikelihoodLoss Function

    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label
    Returns:
        (Array of floats): The derivative values of cost function
    """
    z1 = np.array(A, copy=True)
    y1 = np.array(Y, copy=True)
    y1[y1 == 1] = -1
    return A - Y


def multiclass_perceptron_loss(m, A, Y):
    """Multiclass Perceptron Loss
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
        cost(float): the total loss
    """
    D = np.maximum(A - np.max(Y * A, axis=1).reshape(m, 1), 0)
    cost = (1 / m) * np.sum(np.max(D, axis=1))
    return cost


def multiclass_perceptron_loss_der(m, A, Y):
    """The Derivative of Multiclass Perceptron Loss Function
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
        p(Array of floats): The derivative values of cost function
    """
    # if np.arange(np.shape(A)) == np.argmax(Y*A):
    #    return - np.gradient(np.max(Y*A))
    # elif np.arange(np.shape(A)) != np.argmax(Y*A):
    #   return np.gradient(A)
    # else:
    #   return 0

    p = np.zeros(A.shape)
    p[np.arange(A.shape[0]) == np.argmax(Y * A)] = -np.max(Y * A)
    p[np.arange(A.shape[0]) != np.argmax(Y * A)] = np.gradient(A)[np.arange(A.shape[0]) != np.argmax(Y * A)]
    return p


def multiclass_svm(m, A, Y):
    """Multiclass Weston-Watkins SVM Loss
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label
    Returns:
        cost(float): the total loss
    """
    D = np.maximum(1 + A - np.max(Y * A, axis=1).reshape(m, 1), 0)
    cost = (1 / m) * (np.sum(np.sum(D, axis=1)) - m)
    return cost


def multiclass_svm_der(m, A, Y):
    """The Derivative of Multiclass Weston-Watkins SVM Loss Function
    Parameters:
        m (int):examples no.
        A (float vector): The output y_hat (score)
        Y (float vector): The label
    Returns:
        p (Array of floats): The derivative values of cost function
    """
    # if np.arange(np.shape(A)) == np.argmax(Y*A):
    #    return - np.gradient(np.max(Y*A))
    # elif np.arange(np.shape(A)) != np.argmax(Y*A):
    #    return np.gradient(A)
    # else:
    #    return 0

    p = np.zeros(A.shape)
    p[np.arange(A.shape[0]) == np.argmax(Y * A)] = -np.max(Y * A)
    p[np.arange(A.shape[0]) != np.argmax(Y * A)] = np.gradient(A)[np.arange(A.shape[0]) != np.argmax(Y * A)]
    return p


def multinomial_logistic_loss(m, A, Y):
    """Multinomial Logistic Regression using Softmax Activation
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
        cost(float): the total loss
    """
    cost = np.sum(-np.max(A * Y) + np.log(np.sum(np.exp(A))))
    return cost


def multinomial_logistic_loss_der(m, A, Y):
    """The Derivative of Multinomial Logistic Regression using Softmax Activation Loss Function
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label
    Returns:
        (Array of floats): The derivative values of cost function
    """
    p = np.zeros(A.shape)
    p[Y == 1] = -(1 - A[Y == 1])
    p[Y == 0] = A[Y == 0]
    return p


def square_loss(m, A, Y):
    """Linear Regression Least squares using Identity Activation
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
        cost(float): the total loss
    """
    # return (1/(2*m)) * np.sum(np.dot((A-Y).T,(A-Y)))
    cost = (1 / 2 * m) * np.sum(np.square(Y - A))
    return cost


def square_loss_der(m, A, Y):
    """The Derivative of Linear Regression Least squares using Identity Activation Loss Function
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
    (Array of floats): The derivative values of cost function
    """
    return A - Y


def logistic_sigmoid_loss(m, A, Y):
    """Logistic Regression using sigmoid Activation
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label
    Returns:
        cost(float): the total loss
    """
    cost = (-1 / m) * np.sum(np.log(0.5 * Y - 0.5 + A))
    return cost


def logistic_sigmoid_loss_der(m, A, Y):
    """The Derivative of Logistic Regression using sigmoid Activation Loss Function
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label
    Returns:
        (Array of floats): The derivative values of cost function
    """
    return (- 1) / (0.5 * Y - 0.5 + A)


def logistic_id_loss(m, A, Y):
    """Logistic Regression using Identity Activation
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
        cost(float): the total loss
    """
    cost = (1 / m) * np.sum(np.log(1 + np.exp(- Y * A)))
    return cost


def logistic_id_loss_der(m, A, Y):
    """The Derivative of Logistic Regression using Identity Activation Loss Function
    Parameters:
        m(int):examples no.
        A(float vector): The output y_hat (score)
        Y(float vector): The label

    Returns:
        (Array of floats): The derivative values of cost function
    """
    return - (Y * np.exp(- Y * A)) / (1 + np.exp(- Y * A))


def determine_der_cost_func(func):
    """Determining The Derivative of The Loss function
    Parameters:
        func(string): The Loss function name

    Returns:
        (string): The Derivative of The Loss function
    """
    if func == cross_entropy:
        return cross_entropy_der
    if func == cross_multi_class:
        return cross_multi_class_der
    if func == square_loss:
        return square_loss_der
    if func == perceptron_criteria:
        return perceptron_criteria_der
    if func == svm:
        return svm_der
    if func == multiclass_perceptron_loss:
        return multiclass_perceptron_loss_der
    if func == multiclass_svm:
        return multiclass_svm_der
    if func == multinomial_logistic_loss:
        return multinomial_logistic_loss_der

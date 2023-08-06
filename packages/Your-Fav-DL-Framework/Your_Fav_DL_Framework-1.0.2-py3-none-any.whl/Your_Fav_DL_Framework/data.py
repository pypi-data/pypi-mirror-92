import numpy as np
import matplotlib.pyplot as plt
import pickle


def batch_normlize(x):
    """ This function is used to normalize an array/vector of data
    Parameters:

       x (array/vector): Array/vector of unnormalized numbers
    Returns:

       (array/vector) : normalized array/vector where normalized x = (x - mean) / np.sqrt(variance + eps)
    """
    eps = 0.00001

    mean = x.mean(axis=0)
    variance = x.var(axis=0)

    xnormalized = (x - mean) / np.sqrt(variance + eps)

    return xnormalized


def flatten(x):
    """ This function is used to reshape a matrix into a flat shape.
      usefull in preproccessing of input data
    Parameters:

       x (matrix/vector): Multi-dimension matrix/vector
    Returns:

       (matrix/vector): flatted matrix where each example is in a single row or column
    """
    return x.reshape(x.shape[0], -1).T


def onehot(y_train):
    """ This function is used to change data in the normal form into one-hot form
    Parameters:

       y_train (matrix): Matrix of numbers
    Returns:

       (matrix) : One-hot form of the data
    """


    y = np.zeros((y_train.size, y_train.max() + 1))
    y[np.arange(y_train.size), y_train] = 1
    y = y.T
    return y





class visualize:
    points_y = []
    points_x = []

    fig = plt.figure(figsize=[10, 8])
    graph = fig.subplots()

    def __init__(self, title, y_label, x_label):
        """ visualization class to draw live cost after training, to initialize an instance from this class supply 3 parameters
        Parameters:

           title (string): title of the graph
           y_label (string): label of y coordinate
           x_label (string: label of x coordinate
        """

        self.graph.set_ylabel(y_label)
        self.graph.set_xlabel(x_label)
        self.graph.set_title(title)


def addpoint_y(self, pointy):
    """ This function is used to add a new point to be drawn on a graph
    Parameters:

       pointy (float): value of y coordinate
    Returns:

       graph: graph drawn after adding new point
    """
    self.points_y.append(pointy)

    if (len(self.points_x) == 0):
        self.points_x = [1]

    else:
        self.points_x.append(len(self.points_x) + 1)

    self.graph.plot(self.points_x, self.points_y, 'bo')
    self.fig.show()
    plt.pause(0.0001)


def save(filename, model):
    """ This function saves the model ( all of it's parameters, weights, losses ,... ) in an external file
    Parameters:

       filename (string): Path of file to be saved in, filename must be ".sav" type.
       model    (object): "model" required to be saved.
    Returns:
       (None)
    """
    pickle.dump(model, open(filename, 'wb'))


def retrive(filename):
    """ This function loads a saved model ( all of it's parameters, weights, losses, ...) from external file
    Parameters:

       filename (string): Path of file to be retrived, filename must be ".sav" type.
    Returns:

       (object): Object of model that saved before as whole with its structure(Layers,Nodes,Activation functions)
    """
    return pickle.load(open(filename, 'rb'))
import numpy as np
from Your_Fav_DL_Framework.loss import *
from Your_Fav_DL_Framework.activations import *
from Your_Fav_DL_Framework.eval import *
from Your_Fav_DL_Framework.optmizers import *
from Your_Fav_DL_Framework.data import *


class MultiLayer:
    def __init__(self, number_of_neurons=0, cost_func=cross_entropy):
        """ init of the class multilayer and needed variables
        variables:
            w,b lists for weights
            parameters dic for weights in the form of parameters['W1']
            layers_size for size of each layer
            number_of_input_neurons
            act_func list for activations of each layer
            derivative_act_func list for backward activations derivative functions
            cost_func the choosen cost functions
        parmeters:
            (method) : the cost function of model
        returns:
            (None)
        """
        self.w, self.b = [], []
        self.parameters = {}
        self.layer_size = []

        self.number_of_input_neurons = number_of_neurons
        self.number_of_outputs = 0

        self.act_func = []
        self.derivative_act_func = []

        self.cost_func = cost_func
        self.cost_func_der = determine_der_cost_func(self.cost_func)

        self.cache = {}
        self.prev = []

    def addLayerInput(self, size):
        """ add the input layer of the model
        parmeters:
            size (int) : size of input layer
        retruns:
            (None)
        """
        self.number_of_input_neurons = size
        self.layer_size.append(size)

    def addHidenLayer(self, size, act_func=sigmoid):
        """ add a hidden layer of the model
        parmeters:
            size (int) : size of input layer
            act_func (function) : the activation function of the layer

        retruns:
            (None)
        """
        self.layer_size.append(size)
        self.act_func.append(act_func)
        self.derivative_act_func.append(determine_der_act_func(act_func))

    def addOutputLayer(self, size, act_func=sigmoid):
        """ add the output layer of the model
        parmeters:
            size (int) : size of input layer
            act_func (function) : the activation function of the layer

        retruns:
            (None)
        """
        self.number_of_outputs = size
        self.layer_size.append(size)
        self.act_func.append(act_func)
        self.derivative_act_func.append(determine_der_act_func(act_func))

    def initialize_parameters(self, seed=2):  # ,init_func=random_init_zero_bias):
        """ initialize_weights of the model at the start with xavier init
        parmeters:
            seed (int) : seed for random function
        retruns:
            paramters
        """

        # todo very important check later

        np.random.seed(seed)  # we set up a seed so that your output matches ours although the initialization is random.

        L = len(self.layer_size)  # number of layers in the network

        for l in range(1, L):
            self.w.append(np.random.randn(self.layer_size[l], self.layer_size[l - 1]) * np.sqrt
            (2 / self.layer_size[l - 1]))  # *0.01
            self.b.append(np.zeros((self.layer_size[l], 1)))
            # seed += 1
            # np.random.seed(seed)

        for i in range(len(self.layer_size) - 1):
            self.parameters["W" + str(i + 1)] = self.w[i]
            self.parameters["b" + str(i + 1)] = self.b[i]

        return self.parameters

    def forward_propagation(self, X, drop=0):
        """ forward propagation through the layers
        parmeters:
            X (np.array) : input feature vector
            drop (float) : propablity to keep neurons or shut down

        retruns:
            cashe (dic) : the output of each layer in the form of cashe['Z1']
            Alast (np.array) : last layer activations
        """

        self.prev = []
        self.prev.append((1, X))
        for i in range(len(self.layer_size) - 1):
            Zi = np.dot(self.w[i], self.prev[i][1]) + self.b[i]
            Ai = self.act_func[i](Zi)
            if drop > 0 and i != len(self.layer_size) - 2:
                D = np.random.rand(Ai.shape[0], Ai.shape[1])
                D = D < drop
                Ai = Ai * D
                Ai = Ai / drop

            self.prev.append((Zi, Ai))

        A_last = self.prev[-1][1]

        for i in range(len(self.layer_size) - 1):
            self.cache["Z" + str(i + 1)] = self.prev[i + 1][0]
            self.cache["A" + str(i + 1)] = self.prev[i + 1][1]

        # todo sould i compute cost in here

        return A_last, self.cache

    def set_cost(self, cost_func):
        """ cahnge the initial cost function
        parmeters:
            cost_funct (function) : the new function

        retruns:
            cashe (dic) : the output of each layer in the form of cashe['Z1']
            Alast (np.array) : last layer activations
        """
        self.cost_func = cost_func
        self.cost_func_der = determine_der_cost_func(cost_func)

    def compute_cost(self, Alast, Y):
        """ compute cost of the given examples
        parmeters:
            Alast (np.array) : model predictions
            Y (np.array) : True labels

        retruns:
            cost (float) : cost output
        """
        m = Alast.shape[1]
        return self.cost_func(m, Alast, Y)

    def backward_propagation(self, X, Y):
        """ compute cost of the given examples
        parmeters:
            Alast (np.array) : model predictions
            Y (np.array) : True labels

        retruns:
            grads (dic) : all gridients of wieghts and biasses
        """

        m = X.shape[1]

        # todo all depends on the type of function in cost and actviation function
        grad_list1_w = []
        grad_list1_b = []

        Alast = self.prev[-1][1]
        final_act = self.derivative_act_func[-1]
        dzi = self.cost_func_der(m, Alast, Y) * final_act(Alast)

        if self.cost_func == cross_entropy:
            if self.act_func[-1] == sigmoid:
                pass

        for i in range(len(self.w), 0, -1):
            A = self.prev[i - 1][1]
            dwi = (1 / m) * np.dot(dzi, self.prev[i - 1][1].T)
            dbi = (1 / m) * np.sum(dzi, axis=1, keepdims=True)
            if i != 1:
                der_func = self.derivative_act_func[i - 2]
                A = self.prev[i - 1][1]
                dzi = np.multiply(np.dot((self.w[i - 1]).T, dzi), der_func(A))

            grad_list1_w.append(dwi)
            grad_list1_b.append(dbi)

        # reverse grad list
        grad_list_w = []
        grad_list_b = []

        for i in range(len(grad_list1_w) - 1, -1, -1):
            grad_list_w.append(grad_list1_w[i])
            grad_list_b.append(grad_list1_b[i])

        grads = {}

        for i in range(len(grad_list_w)):
            grads['dW' + str(i + 1)] = grad_list_w[i]
            grads['db' + str(i + 1)] = grad_list_b[i]

        return grads

    def set_cashe(self, cache, X):
        """ set an external cache
        parmeters:
            X (np.array) : input feature vector
            cache (dic) :  output of each layer

        retruns:
            (None)
        """
        self.cache = cache
        self.prev = []
        self.prev.append((1, X))
        for i in range(int(len(cache.keys()) / 2)):
            A, Z = cache["A" + str(i + 1)], cache["Z" + str(i + 1)]
            self.prev.append((Z, A))

    def set_parameters(self, para):
        """ set an external parmeters
        parmeters:
            para (dic) :  the weights and biasses

        retruns:
            (None)
        """
        self.parameters = para
        self.w = []
        self.b = []
        for i in range(int(len(para.keys()) / 2)):
            W, b = para["W" + str(i + 1)], para["b" + str(i + 1)]
            self.w.append(W)
            self.b.append(b)

    def set_parameters_internal(self):
        """ set an internal parmeters this is used by model during training
        parmeters:
            (None)

        retruns:
            (None)
        """
        self.parameters = {}
        for i in range(len(self.w)):
            self.parameters["W" + str(i + 1)] = self.w[i]
            self.parameters["b" + str(i + 1)] = self.b[i]

    def update_parameters(self, grads, learning_rate=1.2, reg_term=0, m=1):
        """ update parameters using grads
        parmeters:
            grads (dic) :  the gradient of weights and biases
            learning_rate (float) : the learn rate hyper parameter
            reg_term (float) : the learn rate hyper parameter

        returns:
            dictionary contains the updated parameters
        """

        for i in range(len(self.w)):
            self.w[i] = (1 - reg_term / m) * self.w[i] - learning_rate * grads["dW" + str(i + 1)]
            self.b[i] = (1 - reg_term / m) * self.b[i] - learning_rate * grads["db" + str(i + 1)]

        self.set_parameters_internal()

        return self.parameters

    def update_parameters_adagrad(self, grads, adagrads, learning_rate=1.2, reg_term=0, m=1):
        """ update parameters using adagrad
        parameters:
            grads (dic) :  the gradient of weights and biases
            adagrads(dic): the square of the gradiant
            learning_rate (float) : the learn rate hyper parameter
            reg_term (float) : the learn rate hyper parameter

        returns:
            dictionary contains the updated parameters
        """

        for i in range(len(self.w)):
            self.w[i] = (1 - reg_term / m) * self.w[i] - (learning_rate / (
            np.sqrt(adagrads["dW" + str(i + 1)]) + 0.000000001)) * grads["dW" + str(i + 1)]
            self.b[i] = (1 - reg_term / m) * self.b[i] - (learning_rate / (
            np.sqrt(adagrads["db" + str(i + 1)]) + 0.000000001)) * grads["db" + str(i + 1)]
        self.set_parameters_internal()

        return self.parameters

    def upadte_patameters_RMS(self, grads, rmsgrads, learning_rate=1.2, reg_term=0, m=1, eps=None):
        """ update parameters using RMS gradient
        parameters:
            grads (dic) :  the gradient of weights and biases
            rmsgrads(dic): taking rho multiplied by the square of previous grads and (1-rho) multiplied by the square of current grads
            learning_rate (float) : the learn rate hyper parameter
            reg_term (float) : the learn rate hyper parameter
            eps(float) : the small value added to rmsgrads to make sure there is no division by zero

        returns:
            dictionary contains the updated parameters
        """

        for i in range(len(self.w)):
            self.w[i] = (1 - reg_term / m) * self.w[i] - (
                                                         learning_rate / (np.sqrt(rmsgrads["dW" + str(i + 1)]) + eps)) * \
                                                         grads["dW" + str(i + 1)]
            self.b[i] = (1 - reg_term / m) * self.b[i] - (
                                                         learning_rate / (np.sqrt(rmsgrads["db" + str(i + 1)]) + eps)) * \
                                                         grads["db" + str(i + 1)]
        self.set_parameters_internal()

        return self.parameters

    def upadte_patameters_adadelta(self, grads, delta, learning_rate=1.2, reg_term=0, m=1):
        """ update parameters using RMS gradient
        parameters:
            grads (dic) :  the gradient of weights and biases, note: this parameter is not used in this function
            delta(dic): dictionary contains the values that should be subtracted from current parameters to be updated
            learning_rate (float) : the learn rate hyper parameter , note: this parameter is not used in this function
            reg_term (float) : the learn rate hyper parameter

        returns:
            dictionary contains the updated parameters
        """

        for i in range(len(self.w)):
            self.w[i] = (1 - reg_term / m) * self.w[i] - delta["dW" + str(i + 1)]
            self.b[i] = (1 - reg_term / m) * self.b[i] - delta["db" + str(i + 1)]
        self.set_parameters_internal()

        return self.parameters

    def update_parameters_adam(self, grads, adamgrads, Fgrads, learning_rate=1.2, reg_term=0, m=1, eps=None):
        """ update parameters using RMS gradient
        parameters:
            grads (dic) :  the gradient of weights and biases , note: grads is not used in this function
            adamgrads(dic): taking rho multiplied by the square of previous grads and (1-rho) multiplied by the square of current grads
            Fgrads(dic): taking rhof multiplied by the  previous grads and (1-rhof) multiplied by the  current grads
            learning_rate (float) : the learn rate hyper parameter (alpha_t not alpha)
            reg_term (float) : the learn rate hyper parameter
            eps(float) : the small value added to adamgrads to make sure there is no division by zero

        returns:
            dictionary contains the updated parameters
        """

        for i in range(len(self.w)):
            self.w[i] = (1 - reg_term / m) * self.w[i] - (learning_rate / np.sqrt(adamgrads["dW" + str(i + 1)] + eps)) * \
                                                         Fgrads["dW" + str(i + 1)]
            self.b[i] = (1 - reg_term / m) * self.b[i] - (learning_rate / np.sqrt(adamgrads["db" + str(i + 1)] + eps)) * \
                                                         Fgrads["db" + str(i + 1)]
        self.set_parameters_internal()

        return self.parameters

    def train(self, X, Y, num_iterations=10000, print_cost=False, print_cost_each=100, cont=0, learning_rate=1,
              reg_term=0, batch_size=0, opt_func=gd_optm, param_dic=None, drop=0):
        """ train giving the data and hpyerparmeters and optmizer type

        parmeters:
            X (np.array) : input feature vector
            Y (np.array) :  the true label
            num_of iterations (int) : how many epochs
            print cost (bool) : to print cost or not
            print cost_each (int) : to print cost each how many iterations
            learning_rate (float) : the learn rate hyper parmeter
            reg_term (float) : the learn rate hyper parmeter
            batch_size (int) : how big is the mini batch and 0 for batch gradint
            optm_func (function) : a function for calling the wanted optmizer

        retruns:
            parmeters (dic) : weights and biasses after training
            cost (float) : cost
        """

        parameters, costs = opt_func(self, X, Y, num_iterations, print_cost, print_cost_each, cont, learning_rate,
                                     reg_term, batch_size, param_dic, drop)
        return parameters, costs

    def predict(self, X):
        """ perdict classes or output
        parmeters:
            X (np.array) :  input feature vector

        retruns:
            Alast (np.array) : output of last layer
        """

        Alast, cache = self.forward_propagation(X)
        # predictions = (Alast > thres) * 1

        return Alast

    def test(self, X, Y, eval_func=accuracy_score):
        """ evalute model
        parmeters:
            X (np.array) :  input feature vector
            Y (np.array) :  the true label
            eval_func (function) : the method of evalution

        retruns:
            Alast (np.array) : output of last layer
        """

        Alast, cache = self.forward_propagation(X)

        acc = eval_func(Alast, Y)

        return acc

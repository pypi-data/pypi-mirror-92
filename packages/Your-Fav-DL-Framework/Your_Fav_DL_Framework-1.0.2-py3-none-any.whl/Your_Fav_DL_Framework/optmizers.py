import numpy as np


def gd_optm(model, X, Y, num_iterations=10000, print_cost=False, print_cost_each=100, cont=0, learning_rate=1,
            reg_term=0, batch_size=0, param_dic=None, drop=0):
    """The function applies the  gradient descent optimizer to update the weight and bias parameters.

    Parameters:

        model (multilayer): instance of the multilayer class contains the models parameters to be updated.
        X: the input feature vector.
        Y: the labels.
        num_iterations: number of epochs.
        print_cost: optional parameter to show the cost function.
        print_cost_each: this parameter is used when "print_cost" is set True to specify when to print the cost ie: after how many iterations.
        cont: not used in this function
        learning_rate: learning rate to be used in updating the parameters.
        reg_term: lamda term added to the loss function to prevent over fitting. This parameter can be set to zero if no regulization is needed.
        batch_size: This parameter is used to specify if the learning process is batch , online or minibatch.
        param_dic: not used in this function.
        drop: dropout parameter to have the option of using the dropout technique.

    Returns:

        dictionary:parameters a dictionary that contains the updated weights and biases
        array:Costs an array that contain the cost of each iteration
    """

    costs = []

    if batch_size == 0:
        for i in range(0, num_iterations):

            Alast, cache = model.forward_propagation(X, drop)  # **

            cost = model.compute_cost(Alast, Y)
            if reg_term != 0:
                for key in model.parameters:
                    cost += (reg_term / X.shape[1]) * np.sum(model.parameters[key] ** 2)

            grads = model.backward_propagation(X, Y)

            parameters = model.update_parameters(grads, learning_rate=learning_rate, reg_term=reg_term, m=X.shape[1])

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs

    else:
        for i in range(0, num_iterations):
            for j in range(int(X.shape[1] / batch_size)):

                Alast, cache = model.forward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size], drop)  # **

                cost = model.compute_cost(Alast, Y[:, j * batch_size:(j * batch_size) + batch_size])
                if reg_term != 0:
                    for key in model.parameters:
                        cost += (reg_term / X[:, j * batch_size:(j * batch_size) + batch_size].shape[1]) * np.sum(
                            model.parameters[key] ** 2)  # **

                grads = model.backward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size],
                                                   Y[:, j * batch_size:(j * batch_size) + batch_size])

                parameters = model.update_parameters(grads, learning_rate=learning_rate, reg_term=reg_term,
                                                     m=X[:, j * batch_size:(j * batch_size) + batch_size].shape[
                                                         1])  # **

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs


def adagrad_optm(model, X, Y, num_iterations=10000, print_cost=False, print_cost_each=100, cont=0, learning_rate=1,
                 reg_term=0, batch_size=0, param_dic=None, drop=0):
    """The function applies the adagrad optimizer to update the weight and bias parameters.

    Parameters:

        model (multilayer): instance of the multilayer class contains the models parameters to be updated.
        X: the input feature vector.
        Y: the labels.
        num_iterations: number of epochs.
        print_cost: optional parameter to show the cost function.
        print_cost_each: this parameter is used when "print_cost" is set True to specify when to print the cost ie: after how many iterations.
        cont: not used in this function
        learning_rate: learning rate to be used in updating the parameters.
        reg_term: lamda term added to the loss function to prevent over fitting. This parameter can be set to zero if no regulization is needed.
        batch_size: This parameter is used to specify if the learning process is batch , online or minibatch.
        param_dic: not used in this function.
        drop: dropout parameter to have the option of using the dropout technique.

    Returns:

        dictionary: parameters a dictionary that contains the updated weights and biases
        array: Costs an array that contain the cost of each iteration
    """
    costs = []
    adagrads = {}

    if batch_size == 0:
        for i in range(0, num_iterations):

            Alast, cache = model.forward_propagation(X, drop)

            cost = model.compute_cost(Alast, Y)
            if reg_term != 0:
                for key in model.parameters:
                    cost += (reg_term / X.shape[1]) * np.sum(model.parameters[key] ** 2)

            grads = model.backward_propagation(X, Y)
            if i == 0:
                for key in grads:
                    adagrads[key] = np.square(grads[key])
            else:
                for key in grads:
                    adagrads[key] = adagrads[key] + np.square(grads[key])

            parameters = model.update_parameters_adagrad(grads, adagrads, learning_rate=learning_rate,
                                                         reg_term=reg_term, m=X.shape[1])

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs

    else:
        for i in range(0, num_iterations):
            for j in range(int(X.shape[1] / batch_size)):

                Alast, cache = model.forward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size], drop)

                cost = model.compute_cost(Alast, Y[:, j * batch_size:(j * batch_size) + batch_size])
                if reg_term != 0:
                    for key in model.parameters:
                        cost += (reg_term / X[:, j * batch_size:(j * batch_size) + batch_size].shape[1]) * np.sum(
                            model.parameters[key] ** 2)

                grads = model.backward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size],
                                                   Y[:, j * batch_size:(j * batch_size) + batch_size])
                if i == 0:
                    for key in grads:
                        adagrads[key] = np.square(grads[key])
                else:
                    for key in grads:
                        adagrads[key] = adagrads[key] + np.square(grads[key])

                parameters = model.update_parameters_adagrad(grads, adagrads, learning_rate=learning_rate,
                                                             reg_term=reg_term,
                                                             m=X[:, j * batch_size:(j * batch_size) + batch_size].shape[
                                                                 1])

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs


def RMS_optm(model, X, Y, num_iterations=10000, print_cost=False, print_cost_each=100, cont=0, learning_rate=1,
             reg_term=0, batch_size=0, param_dic=None, drop=0):
    """The function applies the RMS optimizer to update the weight and bias parameters.

    Parameters:

    model (multilayer): instance of the multilayer class contains the models parameters to be updated.
    X: the input feature vector.
    Y: the labels.
    num_iterations: number of epochs.
    print_cost: optional parameter to show the cost function.
    print_cost_each: this parameter is used when "print_cost" is set True to specify when to print the cost ie: after how many iterations.
    cont: not used in this function
    learning_rate: learning rate to be used in updating the parameters.
    reg_term: lamda term added to the loss function to prevent over fitting. This parameter can be set to zero if no regulization is needed.
    batch_size: This parameter is used to specify if the learning process is batch , online or minibatch.
    param_dic: the dictionary that contains the value of the hyper parameter rho
    drop: dropout parameter to have the option of using the dropout technique.

    Returns:

    dictionary:parameters a dictionary that contains the updated weights and biases
    array:Costs an array that contain the cost of each iteration
    """

    costs = []
    rho = param_dic["rho"]
    eps = param_dic["eps"]
    rmsgrads = {}

    if batch_size == 0:
        for i in range(0, num_iterations):

            Alast, cache = model.forward_propagation(X, drop)

            cost = model.compute_cost(Alast, Y)
            if reg_term != 0:
                for key in model.parameters:
                    cost += (reg_term / X.shape[1]) * np.sum(model.parameters[key] ** 2)

            grads = model.backward_propagation(X, Y)
            if i == 0:
                for key in grads:
                    rmsgrads[key] = (1 - rho) * np.square(grads[key])
            else:
                for key in grads:
                    rmsgrads[key] = (rho) * rmsgrads[key] + (1 - rho) * np.square(grads[key])

            parameters = model.upadte_patameters_RMS(grads, rmsgrads, learning_rate=learning_rate, reg_term=reg_term,
                                                     m=X.shape[1], eps=eps)

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs

    else:
        for i in range(0, num_iterations):
            for j in range(int(X.shape[1] / batch_size)):

                Alast, cache = model.forward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size], drop)

                cost = model.compute_cost(Alast, Y[:, j * batch_size:(j * batch_size) + batch_size])
                if reg_term != 0:
                    for key in model.parameters:
                        cost += (reg_term / X[:, j * batch_size:(j * batch_size) + batch_size].shape[1]) * np.sum(
                            model.parameters[key] ** 2)

                grads = model.backward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size],
                                                   Y[:, j * batch_size:(j * batch_size) + batch_size])
                if i == 0:
                    for key in grads:
                        rmsgrads[key] = np.square(grads[key])
                else:
                    for key in grads:
                        rmsgrads[key] = (rho) * rmsgrads[key] + (1 - rho) * np.square(grads[key])

                parameters = model.upadte_patameters_RMS(grads, rmsgrads, learning_rate=learning_rate,
                                                         reg_term=reg_term,
                                                         m=X[:, j * batch_size:(j * batch_size) + batch_size].shape[1],
                                                         eps=eps)

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs


def adadelta_optm(model, X, Y, num_iterations=10000, print_cost=False, print_cost_each=100, cont=0, learning_rate=1,
                  reg_term=0, batch_size=0, param_dic=None, drop=0):
    """The function applies the adadelta optimizer to update the weight and bias parameters.

    Parameters:

        model (multilayer): instance of the multilayer class contains the models parameters to be updated.
        X: the input feature vector.
        Y: the labels.
        num_iterations: number of epochs.
        print_cost: optional parameter to show the cost function.
        print_cost_each: this parameter is used when "print_cost" is set True to specify when to print the cost ie: after how many iterations.
        cont: not used in this function
        learning_rate: learning rate to be used in updating the parameters.
        reg_term: lamda term added to the loss function to prevent over fitting. This parameter can be set to zero if no regulization is needed.
        batch_size: This parameter is used to specify if the learning process is batch , online or minibatch.
        param_dic: the dictionary that contains the value of the hyper parameters rho and epsilon.
        drop: dropout parameter to have the option of using the dropout technique.

    Returns:

        dictionary: parameters a dictionary that contains the updated weights and biases
        array: Costs an array that contain the cost of each iteration
    """

    costs = []
    rho = param_dic["rho"]
    eps = param_dic["eps"]
    adadeltagrads = {}
    segma = {}
    delta = {}

    if batch_size == 0:
        for i in range(0, num_iterations):

            Alast, cache = model.forward_propagation(X, drop)

            cost = model.compute_cost(Alast, Y)
            if reg_term != 0:
                for key in model.parameters:
                    cost += (reg_term / X.shape[1]) * np.sum(model.parameters[key] ** 2)

            grads = model.backward_propagation(X, Y)
            if i == 0:
                for key in grads:
                    adadeltagrads[key] = np.square(grads[key])
                    segma[key] = (np.random.randn(grads[key].shape[0], grads[key].shape[1]) + 2)
                    delta[key] = np.sqrt(segma[key] / (adadeltagrads[key]) + eps) * grads[key]
            else:
                for key in grads:
                    adadeltagrads[key] = adadeltagrads[key] + np.square(grads[key])
                    segma[key] = (rho) * segma[key] + (1 - rho) * np.square(delta[key])
                    delta[key] = np.sqrt(segma[key] / (adadeltagrads[key]) + eps) * grads[key]

            parameters = model.upadte_patameters_adadelta(grads, delta, learning_rate=learning_rate, reg_term=reg_term,
                                                          m=X.shape[1])

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs

    else:
        for i in range(0, num_iterations):
            for j in range(int(X.shape[1] / batch_size)):

                Alast, cache = model.forward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size], drop)

                cost = model.compute_cost(Alast, Y[:, j * batch_size:(j * batch_size) + batch_size])
                if reg_term != 0:
                    for key in model.parameters:
                        cost += (reg_term / X[:, j * batch_size:(j * batch_size) + batch_size].shape[1]) * np.sum(
                            model.parameters[key] ** 2)

                grads = model.backward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size],
                                                   Y[:, j * batch_size:(j * batch_size) + batch_size])
                if i == 0:
                    for key in grads:
                        adadeltagrads[key] = np.square(grads[key])
                        segma[key] = (np.random.randn(grads[key].shape[0], grads[key].shape[1]) + 100) * 0.00001
                        delta[key] = np.sqrt(segma[key] / (adadeltagrads[key]) + eps) * grads[key]
                else:
                    for key in grads:
                        adadeltagrads[key] = adadeltagrads[key] + np.square(grads[key])
                        segma[key] = (rho) * segma[key] + (1 - rho) * np.square(delta[key])
                        delta[key] = np.sqrt(segma[key] / (adadeltagrads[key]) + eps) * grads[key]

                parameters = model.upadte_patameters_adadelta(grads, delta, learning_rate=learning_rate,
                                                              reg_term=reg_term, m=
                                                              X[:, j * batch_size:(j * batch_size) + batch_size].shape[
                                                                  1])

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs


def adam_optm(model, X, Y, num_iterations=10000, print_cost=False, print_cost_each=100, cont=0, learning_rate=1,
              reg_term=0, batch_size=0, param_dic=None, drop=0):
    """The function applies the adam optimizer to update the weight and bias parameters.

    Parameters:

        model (multilayer): instance of the multilayer class contains the models parameters to be updated.
        X: the input feature vector.
        Y: the labels.
        num_iterations: number of epochs.
        print_cost: optional parameter to show the cost function.
        print_cost_each: this parameter is used when "print_cost" is set True to specify when to print the cost ie: after how many iterations.
        cont: not used in this function
        learning_rate: learning rate to be used in updating the parameters.
        reg_term: lamda term added to the loss function to prevent over fitting. This parameter can be set to zero if no regulization is needed.
        batch_size: This parameter is used to specify if the learning process is batch , online or minibatch.
        param_dic: the dictionary that contains the value of the hyper parameters rho , rhof and epsilon.
        drop: dropout parameter to have the option of using the dropout technique.

    Returns:

        dictionary:parameters a dictionary that contains the updated weights and biases
        array:Costs an array that contain the cost of each iteration
       """

    costs = []
    rho = param_dic["rho"]
    eps = param_dic["eps"]
    rhof = param_dic["rhof"]
    adamgrads = {}
    Fgrads = {}
    if batch_size == 0:
        for i in range(0, num_iterations):

            Alast, cache = model.forward_propagation(X, drop)

            cost = model.compute_cost(Alast, Y)
            if reg_term != 0:
                for key in model.parameters:
                    cost += (reg_term / X.shape[1]) * np.sum(model.parameters[key] ** 2)

            grads = model.backward_propagation(X, Y)
            if i == 0:
                for key in grads:
                    adamgrads[key] = (1 - rho) * np.square(grads[key])
                    Fgrads[key] = (1 - rhof) * grads[key]

            else:
                for key in grads:
                    adamgrads[key] = (rho) * adamgrads[key] + (1 - rho) * np.square(grads[key])
                    Fgrads[key] = (rho) * Fgrads[key] + (1 - rhof) * grads[key]
            alpha_t = learning_rate * np.sqrt((1 - rho ** (num_iterations)) / (1 - rhof ** (num_iterations)))

            parameters = model.update_parameters_adam(grads, adamgrads, Fgrads, learning_rate=alpha_t,
                                                      reg_term=reg_term, m=X.shape[1], eps=eps)

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs

    else:
        for i in range(0, num_iterations):
            for j in range(int(X.shape[1] / batch_size)):

                Alast, cache = model.forward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size], drop)

                cost = model.compute_cost(Alast, Y[:, j * batch_size:(j * batch_size) + batch_size])
                if reg_term != 0:
                    for key in model.parameters:
                        cost += (reg_term / X[:, j * batch_size:(j * batch_size) + batch_size].shape[1]) * np.sum(
                            model.parameters[key] ** 2)

                grads = model.backward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size],
                                                   Y[:, j * batch_size:(j * batch_size) + batch_size])
                if i == 0:
                    for key in grads:
                        adamgrads[key] = (1 - rho) * np.square(grads[key])
                        Fgrads[key] = (1 - rhof) * grads[key]
                else:
                    for key in grads:
                        adamgrads[key] = (rho) * adamgrads[key] + (1 - rho) * np.square(grads[key])
                        Fgrads[key] = (rho) * Fgrads[key] + (1 - rhof) * grads[key]
                alpha_t = learning_rate * np.sqrt((1 - rho ** (num_iterations)) / (1 - rhof ** (num_iterations)))

                parameters = model.update_parameters_adam(grads, adamgrads, Fgrads, learning_rate=alpha_t,
                                                          reg_term=reg_term,
                                                          m=X[:, j * batch_size:(j * batch_size) + batch_size].shape[1],
                                                          eps=eps)

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs


def mom_optm(model, X, Y, num_iterations=10000, print_cost=False, print_cost_each=100, cont=0, learning_rate=1,
             reg_term=0, batch_size=0, param_dic=None, drop=0):
    """The function applies the momentum optimizer to update the weight and bias parameters.

    Parameters:

        model (multilayer): instance of the multilayer class contains the models parameters to be updated.
        X: the input feature vector.
        Y: the labels.
        num_iterations: number of epochs.
        print_cost: optional parameter to show the cost function.
        print_cost_each: this parameter is used when "print_cost" is set True to specify when to print the cost ie: after how many iterations.
        cont: not used in this function
        learning_rate: learning rate to be used in updating the parameters.
        reg_term: lamda term added to the loss function to prevent over fitting. This parameter can be set to zero if no regulization is needed.
        batch_size: This parameter is used to specify if the learning process is batch , online or minibatch.
        param_dic: the dictionary that contains the value of the hyper parameters beta.
        drop: dropout parameter to have the option of using the dropout technique.

    Returns:

        dictionary:parameters a dictionary that contains the updated weights and biases
        array:Costs an array that contain the cost of each iteration
           """

    costs = []

    beta = param_dic['beta']
    momen_grad = {}

    if batch_size == 0:
        for i in range(0, num_iterations):

            Alast, cache = model.forward_propagation(X, drop)
            cost = model.compute_cost(Alast, Y)
            if reg_term != 0:
                for key in model.parameters:
                    cost += (reg_term / X.shape[1]) * np.sum(model.parameters[key] ** 2)

            grads = model.backward_propagation(X, Y)

            if i == 0:
                for key in grads:
                    momen_grad[key] = (1 - beta) * grads[key]
            else:
                for key in grads:
                    momen_grad[key] = beta * momen_grad[key] + (1 - beta) * grads[key]

            parameters = model.update_parameters(momen_grad, learning_rate=learning_rate, reg_term=reg_term,
                                                 m=X.shape[1])

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs

    else:
        for i in range(0, num_iterations):
            for j in range(int(X.shape[1] / batch_size)):

                Alast, cache = model.forward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size], drop)

                cost = model.compute_cost(Alast, Y[:, j * batch_size:(j * batch_size) + batch_size])
                if reg_term != 0:
                    for key in model.parameters:
                        cost += (reg_term / X[:, j * batch_size:(j * batch_size) + batch_size].shape[1]) * np.sum(
                            model.parameters[key] ** 2)

                grads = model.backward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size],
                                                   Y[:, j * batch_size:(j * batch_size) + batch_size])

                if i == 0:
                    for key in grads:
                        momen_grad[key] = (1 - beta) * grads[key]
                else:
                    for key in grads:
                        momen_grad[key] = beta * momen_grad[key] + (1 - beta) * grads[key]

                parameters = model.update_parameters(momen_grad, learning_rate=learning_rate, reg_term=reg_term,
                                                     m=X[:, j * batch_size:(j * batch_size) + batch_size].shape[1])

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs


def gd_optm_steepst(model, X, Y, num_iterations=10000, print_cost=False, print_cost_each=100, cont=0,
                    learning_rate=0.01, reg_term=0, batch_size=0, param_dic=None, drop=0):
    """The function applies the steepest gradient descent optimizer to update the weight and bias parameters.

    Parameters:

        model (multilayer): instance of the multilayer class contains the models parameters to be updated.
        X: the input feature vector.
        Y: the labels.
        num_iterations: number of epochs.
        print_cost: optional parameter to show the cost function.
        print_cost_each: this parameter is used when "print_cost" is set True to specify when to print the cost ie: after how many iterations.
        cont: not used in this function
        learning_rate: learning rate to be used in updating the parameters.
        reg_term: lamda term added to the loss function to prevent over fitting. This parameter can be set to zero if no regulization is needed.
        batch_size: This parameter is used to specify if the learning process is batch , online or minibatch.
        param_dic: not used in this function.
        drop: dropout parameter to have the option of using the dropout technique.

    Returns:

        dictionary:parameters a dictionary that contains the updated weights and biases
        array:Costs an array that contain the cost of each iteration
           """
    costs = []

    if batch_size == 0:
        for i in range(0, num_iterations):

            Alast, cache = model.forward_propagation(X, drop)  # **

            cost = model.compute_cost(Alast, Y)
            if reg_term != 0:
                for key in model.parameters:
                    cost += (reg_term / X.shape[1]) * np.sum(model.parameters[key] ** 2)

            grads = model.backward_propagation(X, Y)
            m = Alast.shape[1]
            learning_rate = 100 * np.amin((- 1 / m) * (
            Y * np.log(np.abs(Alast - (learning_rate * model.cost_func_der(m, Alast, Y)))) + (1 - Y) * (
            np.log(np.abs(1 - (Alast - learning_rate * model.cost_func_der(m, Alast, Y)))))))

            parameters = model.update_parameters(grads, learning_rate=learning_rate, reg_term=reg_term, m=X.shape[1])

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs

    else:
        for i in range(0, num_iterations):
            for j in range(int(X.shape[1] / batch_size)):

                Alast, cache = model.forward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size], drop)  # **

                cost = model.compute_cost(Alast, Y[:, j * batch_size:(j * batch_size) + batch_size])
                if reg_term != 0:
                    for key in model.parameters:
                        cost += (reg_term / X[:, j * batch_size:(j * batch_size) + batch_size].shape[1]) * np.sum(
                            model.parameters[key] ** 2)  # **
                grads = model.backward_propagation(X[:, j * batch_size:(j * batch_size) + batch_size],
                                                   Y[:, j * batch_size:(j * batch_size) + batch_size])
                m = Alast.shape[1]
                learning_rate = 100 * np.amin((- 1 / m) * (
                Y * np.log(np.abs(Alast - (learning_rate * model.cost_func_der(m, Alast, Y)))) + (1 - Y) * (
                np.log(np.abs(1 - (Alast - learning_rate * model.cost_func_der(m, Alast, Y)))))))

                parameters = model.update_parameters(grads, learning_rate=learning_rate, reg_term=reg_term,
                                                     m=X[:, j * batch_size:(j * batch_size) + batch_size].shape[
                                                         1])  # **

            if print_cost and i % print_cost_each == 0:
                costs.append(cost)
                print("Cost after iteration %i: %f" % (i, cost))

        return parameters, costs

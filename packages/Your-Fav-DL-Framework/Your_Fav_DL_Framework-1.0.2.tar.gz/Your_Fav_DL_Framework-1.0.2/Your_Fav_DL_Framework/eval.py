import numpy as np
import seaborn as sns
import matplotlib.pylab as plt


def conf_mat (A,Y,thres=0.5):
    '''This function calculates the confusion matrix from predicted and truth matrices
    Parameters:
        A (numpy matrix): predicted classification for each example
        Y (numpy matrix): true classification for each example
        thres (float): threshold value, values above it are considered true
    Returns:
        (numpy matrix): confusion matrix
    '''

    if Y.shape[0] == 1:
        predictions = (A > thres) * 1
        confusion_matrix =np.zeros((2,2))
        confusion_matrix[0][0] =float(np.dot(Y, predictions.T))
        confusion_matrix[0][1] =float(np.dot(1-Y, predictions.T))
        confusion_matrix[1][0] =float(np.dot(Y, 1-predictions.T))
        confusion_matrix[1][1] =float(np.dot(1-Y, 1-predictions.T))
    else:
        predectin = A.argmax(axis=0) #tuble containing predction of each example
        truth = Y.argmax(axis=0)     #tuble containing truth of each example
        confusion_matrix= np.zeros((Y.shape[0],Y.shape[0]))
        for i in range(0,Y.shape[1]):
            confusion_matrix[truth[i]][predectin [i]]+=1

    return confusion_matrix

def print_conf_mat(A,Y,thres=0.5):
    '''This function prints the confusion matrix from predicted and truth matrices
    Parameters:
        A (numpy matrix): predicted classification for each example
        Y (numpy matrix): true classification for each example
        thres (float) : threshold value, values above it are considered true
    '''
    ax = sns.heatmap(conf_mat(A,Y), annot=True, linewidth=0.5)
    plt.show()

def conf_table(cnf_matrix):
    '''Tis function calculates the confusion table from confusion matrix
    Parameters:
        cnf_matrix (numpy matrix): confusion matrix
    Returns:
        (tuple of floats): representing TP for each class
        (tuple of floats): representing FP for each class
        (tuple of floats): representing TN for each class
        (tuple of floats): representing FN for each class
    '''
    FP = cnf_matrix.sum(axis=0) - np.diag(cnf_matrix)
    FN = cnf_matrix.sum(axis=1) - np.diag(cnf_matrix)
    TP = np.diag(cnf_matrix)
    TN = cnf_matrix.sum() - (FP + FN + TP)
    FP = FP.astype(float)
    FN = FN.astype(float)
    TP = TP.astype(float)
    TN = TN.astype(float)

    return FP,FN,TP,TN

def accuracy_score(A,Y,thres=0.5):
    '''This function calculates the accuracy of the model using predicted and truth values
    Parameters:
        A (numpy matrix): predicted classification for each example
        Y (numpy matrix): true classification for each example
        thres (float): threshold value, values above it are considered true
    Returns:
        (float): accuracy
    '''
    if Y.shape[0] == 1:
        predictions = (A > thres) * 1
        ACC = float((np.dot(Y,predictions.T) + np.dot(1-Y,1-predictions.T))/float(Y.size))
    else:
        FP, FN, TP, TN = conf_table(conf_mat(A, Y))
        ACC = (TP + TN+0.00000000001) / (TP + FP + FN + TN+0.00000000001)
        ACC = np.sum(ACC) / ACC.shape[0]

    return ACC * 100

def precision_score(A, Y, thres=0.5):
    '''This function calculates the precision of the model using predicted and truth values
    Parameters:
        A (numpy matrix): predicted classification for each example
        Y (numpy matrix): true classification for each example
        thres (float): threshold value, values above it are considered true
    Returns:
        (float): precision
    '''
    if Y.shape[0] == 1:
        predictions = (A > thres) * 1
        prec = float(np.dot(Y,predictions.T)/float(np.dot(Y,predictions.T)+np.dot(1-Y,predictions.T)))
    else:
        FP, FN, TP, TN = conf_table(conf_mat(A, Y))
        prec = (TP+0.00000000001)/(TP + FP+0.00000000001)
        prec = np.sum(prec) / prec.shape[0]
    return prec * 100


def recall_score(A,Y,thres=0.5):
    '''This function calculates the recall of the model using predicted and truth values
    Parameters:
        A (numpy matrix): predicted classification for each example
        Y (numpy matrix): true classification for each example
        thres (float): threshold value, values above it are considered true
    Returns:
        (float): recall
    '''

    if Y.shape[0] == 1:
        predictions = (A > thres) * 1
        rec = float(np.dot(Y,predictions.T)/float(np.dot(Y,predictions.T)+np.dot(Y,1-predictions.T)))
    else:
        FP, FN, TP, TN = conf_table(conf_mat(A, Y))
        rec = (TP+0.00000000001) / (TP + FN+0.00000000001)
        rec = np.sum(rec) / rec.shape[0]

    return rec * 100

def f1_score(A,Y,thres=0.5):
    '''This function calculates the f1_score of the model using predicted and truth values
    Parameters:
        A (numpy matrix): predicted classification for each example
        Y (numpy matrix): true classification for each example
        thres (float) : threshold value, values above it are considered true
    Returns:
        (float): f1_score
    '''

    prec=precision_score(A, Y)
    rec=recall_score(A,Y)
    f1=float((2*prec*rec)/float(prec+rec))
    return f1
import numpy as np


def accuracy_score(y_act, y_pred):
    '''Computes accuracy.

    Args:
        y_act: actual labels:
        y_pred: predicted labels.
    Returns:
        accuracy
    '''
    y_act = np.squeeze(y_act)
    y_pred = np.squeeze(y_pred)
    return np.mean(y_act == y_pred)

	
def mean_absolute_error(y_act, y_pred):
    '''Computes mean absolute error.

    Args:
        y_act: actual labels:
        y_pred: predicted labels.  
    Returns:
        mean absolute error
    '''
    y_act = np.squeeze(y_act)
    y_pred = np.squeeze(y_pred)
    return np.mean(np.absolute(y_act - y_pred))


def mean_squared_error(y_act, y_pred):
    '''Computes mean squared error.

    Args:
        y_act: actual labels:
        y_pred: predicted labels.  
    Returns:
        mean squared error
    '''
    y_act = np.squeeze(y_act)
    y_pred = np.squeeze(y_pred)
    return np.mean(np.square(y_act - y_pred))

def root_mean_square_error(y_act, y_pred):
    '''Computes root mean square error.

    Args:
        y_act: actual labels:
        y_pred: predicted labels.
    Returns:
        root mean square error
    '''
    y_act = np.squeeze(y_act)
    y_pred = np.squeeze(y_pred)
    return np.mean( np.sqrt( np.square(y_act - y_pred) ) )



def compute_score(y_act, y_pred, name):
    '''computes the score of a specified type.

    Args:
        y_act: actual labels:
        y_pred: predicted labels.
        name: type of score to apply.
    Returns:
        the score of the specified type.
    '''
    if name =='accuracy':
        return accuracy_score(y_act, y_pred)
    elif name == 'mean-absolute-error':
        return mean_absolute_error(y_act, y_pred)
    elif name == 'mean-squared-error':
        return mean_squared_error(y_act, y_pred)
    elif name == 'root-mean-square-error':
        return root_mean_square_error(y_act, y_pred)
    elif name == 'precision':
        return precision_score(y_act, y_pred)
    elif name == 'recall':
        return recall_score(y_act, y_pred)
    elif name == 'f1-score':
        return f1_score(y_act, y_pred)

def compute_tp_tn_fp_fn(y_act, y_pred):
    '''Computes - True Positive (TP), True Negative (TN), False Positive (FP), False Negative (FN).

    Args:
        y_act: actual labels:
        y_pred: predicted labels.
    Returns:
        True Positive (TP), True Negative (TN), False Positive (FP), False Negative (FN)
    '''
    y_act = np.squeeze(y_act)
    y_pred = np.squeeze(y_pred)
    tp = sum((y_act == 1) & (y_pred == 1))
    tn = sum((y_act == 0) & (y_pred == 0))
    fp = sum((y_act == 0) & (y_pred == 1))
    fn = sum((y_act == 1) & (y_pred == 0))
    return tp, tn, fp, fn



def precision_score(y_act, y_pred):
    '''Calculates the Precision (Precision = TP  / FP + TP ) .

    Args:
        y_act: actual labels:
        y_pred: predicted labels.        
    Returns:
        recall.
    '''
    tp, tn, fp, fn = compute_tp_tn_fp_fn(y_act, y_pred)
    return tp / float( tp + fp)


def recall_score(y_act, y_pred):
    '''Calculates the Recall (Recall = TP /FN + TP) .

    Args:
        y_act: actual labels:
        y_pred: predicted labels.        
    Returns:
        recall.
    '''
    tp, tn, fp, fn = compute_tp_tn_fp_fn(y_act, y_pred)
    return tp / float( tp + fn)

def f1_score(y_act, y_pred):
    '''Calculates the F1 score.

    Args:
        y_act: actual labels:
        y_pred: predicted labels.
    Returns:
        F1 score.
    '''
    tp, tn, fp, fn = compute_tp_tn_fp_fn(y_act, y_pred)
    precision = precision_score(y_act, y_pred)
    recall = recall_score(y_act, y_pred)
    f1_score = (2*precision*recall)/ (precision + recall)
    return f1_score
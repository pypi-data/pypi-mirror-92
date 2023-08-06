import numpy as np 
import pickle


def split_train_test(data, test_ratio):
    '''Splits data to train and test.

    Args:
        data: data to be splitted.
        test_ratio: ratio of test data.
        
    Returns:
        train data, test data as a tuple.
    '''
    m = data.shape[1]
    shuffled_indices = np.random.permutation(m)
    test_set_size = int(m * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data[:, train_indices], data[:, test_indices]

def save(data, file):
    '''Writes the date to a provided file.

    Args:
        data: the data to be saved.
        file: the file to save the data to.
    '''
    with open(file, "wb") as f:
        pickle.dump(data, f)


def load(file):
    '''Loads data as numpy array from a provided files.

    Args:
        file: the file to load the data from.
    Returns:
        The data.
    '''
    with open(file, "rb") as f:
        data = pickle.load(f)
    return data


def rescalling(data, scale):
    '''rescalls the data.

    Args:
        scale:
    Returns:
        The data after scalling.
    '''
    return data * scale

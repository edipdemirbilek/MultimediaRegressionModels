# -*- coding: utf-8 -*-
"""
@author: edip.demirbilek

Dataset Utils..

This module allow us to process the Parametric and Bitstream version of the
INRS Audiovisual Quality Dataset.

Todo:
    * Read parametric version of the INRS Audiovisual Quality Dataset.
"""
import random
import pandas as pd
from numpy import array, asarray

SORTED_DATASET_FILE_NAME = \
    "./dataset/rf_sorted/bitstream_dataset_columns_sorted.csv"
SORTED_SUBJECTS_DATASET_FILE_NAME = \
    "./dataset/rf_sorted/bitstream_subjects_dataset_columns_sorted.csv"
PCA_FEATURES_FILE_PREFIX = "./dataset/pca_extracted/pca_"
FAST_ICA_FEATURES_FILE_PREFIX = "./dataset/fast_ica_extracted/fast_ica_"
INCREMENTAL_PCA_FEATURES_FILE_PREFIX = \
    "./dataset/incremental_pca_extracted/incremental_pca_"
KERNEL_PCA_FEATURES_FILE_PREFIX = "./dataset/kernel_pca_extracted/kernel_pca_"


def pack_partitioned_data(x_train, x_test, y_train, y_test, ci_high, ci_low):
    """
    Packs training and test data, and confidence intervals.

    Arguments:
        x_train -- Training attributes,
            numpy.ndarray of shape (training_size, n_features)
        x_test -- Test attributes,
            numpy.ndarray of shape (test_size, n_features)
        y_train -- Training labels, numpy.ndarray of shape (training_size, )
        y_test -- Test labels, numpy.ndarray of shape (test_size, )
        ci_high -- 95% Confidence Interval high values,
            numpy.ndarray of shape (test_size, 1)
        ci_low -- 95% Confidence Interval low values,
            numpy.ndarray of shape (test_size, 1)

    Returns:
        partitioned_data -- Dictionary of shape:
            {
                'x_train': x_train,
                'x_test': x_test,
                'y_train': y_train,
                'y_test': y_test,
                'ci_high': ci_high,
                'ci_low': ci_low
            }
    """
    partitioned_data = {}
    partitioned_data["x_train"] = x_train
    partitioned_data["x_test"] = x_test
    partitioned_data["y_train"] = y_train
    partitioned_data["y_test"] = y_test
    partitioned_data["ci_high"] = ci_high
    partitioned_data["ci_low"] = ci_low

    return partitioned_data


def unpack_partitioned_data(partitioned_data):
    """
    Unpacks training and test data, and confidence intervals.

    Arguments:
        partitioned_data -- Dictionary of shape:
            {
                'x_train': x_train,
                'x_test': x_test,
                'y_train': y_train,
                'y_test': y_test,
                'ci_high': ci_high,
                'ci_low': ci_low
            }

    Returns:
        x_train -- Training attributes,
            numpy.ndarray of shape (training_size, n_features)
        x_test -- Test attributes,
            numpy.ndarray of shape (test_size, n_features)
        y_train -- Training labels, numpy.ndarray of shape (training_size, )
        y_test -- Test labels, numpy.ndarray of shape (test_size, )
        ci_high -- 95% Confidence Interval high values,
            numpy.ndarray of shape (test_size, 1)
        ci_low -- 95% Confidence Interval low values,
            numpy.ndarray of shape (test_size, 1)
    """
    x_train = partitioned_data["x_train"]
    x_test = partitioned_data["x_test"]
    y_train = partitioned_data["y_train"]
    y_test = partitioned_data["y_test"]
    ci_high = partitioned_data["ci_high"]
    ci_low = partitioned_data["ci_low"]
    return x_train, x_test, y_train, y_test, ci_high, ci_low


def load_dataset(f_type, n_features):
    """
    Reads and shuffles dataset from file DATASET_FILE_NAME and returns
    attributes(data) and labels.

    Arguments:
        f_type -- type of features to load. rf sorted vs pca extarcted
        n_features -- number of features, only is f_type=pca

    Returns:
        attributes -- Attributes(data), list of size data_size x n_featurees
        labels -- Labels, list of size data_size
    """
    # arrange data into list for labels and list of lists for attributes
    attributes_tmp = []
    first_row = True

    file_name = SORTED_DATASET_FILE_NAME
    if(f_type == "pca"):
        file_name = PCA_FEATURES_FILE_PREFIX+str(n_features)+".csv"
    elif(f_type == "fast_ica"):
        file_name = FAST_ICA_FEATURES_FILE_PREFIX+str(n_features)+".csv"
    elif(f_type == "incremental_pca"):
        file_name = INCREMENTAL_PCA_FEATURES_FILE_PREFIX+str(n_features)+".csv"
    elif(f_type == "kernal_pca"):
        file_name = KERNEL_PCA_FEATURES_FILE_PREFIX+str(n_features)+".csv"

    print("Reading from file: "+file_name)

    with open(file_name) as file:
        for line in file:
            # split on comma
            row = line.strip().split(",")
            if first_row:
                first_row = False
                continue
            attributes_tmp.append(row)

    random.shuffle(attributes_tmp)

    # Separate attributes and labels
    attributes = []
    labels = []
    for row in attributes_tmp:
        labels.append(float(row.pop()))
        row_length = len(row)
        # eliminate ID
        attributes_one_row = [float(row[i]) for i in range(0, row_length)]
        attributes.append(attributes_one_row)

    # number of rows and columns in x matrix
    nrows = len(attributes)
    ncols = len(attributes[1])
    print("#Rows: " + str(nrows) + " #Cols: " + str(ncols))

    return attributes, labels


def partition_data(attributes, train_index, test_index, labels, n_features,
                   f_type):
    """
    Partition attributes(data) and labels into training and test data using
    train and test indexes provided and packs them into partitioned_data.

    Arguments:
        attributes -- Attributes(data), list of size data_size x n_featurees
        train_index -- Training Indexes, numpy.ndarray of size (train_size, )
        test_index -- Test Indexes, numpy.ndarray of size (test_size, )
        labels -- Labels, list of size data_size
        n_features -- Number of features, int
        f_type -- only used when value is 'sorted_subjects'

    Returns:
        partitioned_data -- Partitioned data, Dictionary of shape:
            {
                'x_train': x_train,
                'x_test': x_test,
                'y_train': y_train,
                'y_test': y_test,
                'ci_high': ci_high,
                'ci_low': ci_low
            }
            here:
                x_train -- Training attributes,
                    numpy.ndarray of shape (training_size, n_features)
                x_test -- Test attributes, \
                    numpy.ndarray of shape (test_size, n_features)
                y_train -- Training labels, numpy.ndarray of shape
                    (training_size, )
                y_test -- Test labels, numpy.ndarray of shape (test_size, )
                ci_high -- 95% Confidence Interval high values,
                    numpy.ndarray of shape (test_size, 1)
                ci_low -- 95% Confidence Interval low values,
                    numpy.ndarray of shape (test_size, 1)
    """
    x_train_all_attributes, x_test_all_attributes, y_train, y_test \
        = [attributes[i] for i in train_index], \
          [attributes[i] for i in test_index], \
          [labels[i] for i in train_index], \
          [labels[i] for i in test_index]

    if (f_type == 'sorted_subjects'):
        x_train_all_attributes, y_train \
            = substitute_training_data(x_train_all_attributes, y_train)

    x_train = []
    x_test = []
    ci_high = []
    ci_low = []

    for x_train_row in x_train_all_attributes:
        x_train.append(x_train_row[0:n_features])

    for x_test_row in x_test_all_attributes:
        x_test.append(x_test_row[0:n_features])
        ci_high.append(x_test_row[-2:-1])
        ci_low.append(x_test_row[-1:])

    partitioned_data = pack_partitioned_data(asarray(x_train), asarray(x_test),
                                             asarray(y_train), asarray(y_test),
                                             asarray(ci_high), asarray(ci_low))

    return partitioned_data


def normalize_data(partitioned_data):
    """
    Normalize training and test data, and confidence interval values.

    Arguments:
        partitioned_data -- Partitioned data, Dictionary of shape:
            {
                'x_train': x_train,
                'x_test': x_test,
                'y_train': y_train,
                'y_test': y_test,
                'ci_high': ci_high,
                'ci_low': ci_low
            }

    Returns:
        partitioned_data -- Partitioned data, Dictionary of shape:
            {
                'x_train': x_train normalized (0 mean and 1 variance)
                'x_test': x_test normalized (0 mean and 1 variance)
                'y_train': y_train/5
                'y_test': y_test/5
                'ci_high': ci_high normalized (0 mean and 1 variance)
                'ci_low': ci_low normalized (0 mean and 1 variance)
            }
    """
    x_train, x_test, y_train, y_test, ci_high, ci_low \
        = unpack_partitioned_data(partitioned_data)

    # This is for 0 mean and 1 variance
    x_mean, x_std = x_train.mean(axis=0), x_train.std(axis=0)
    x_train = (x_train - x_mean)/x_std
    x_test = (x_test - x_mean)/x_std

    # This is for normalization
    y_train = y_train/5
    y_test = y_test/5
    ci_low = array(ci_low)/5
    ci_high = array(ci_high)/5

    x_train = array(x_train)
    y_train = array(y_train)
    x_test = array(x_test)
    y_test = array(y_test)

    partitioned_data = pack_partitioned_data(x_train, x_test, y_train,
                                             y_test, ci_high, ci_low)

    return partitioned_data


def prepare_data(attributes, train_index, test_index, labels, n_features,
                 f_type):
    """
    Partition and normalize data.

    Arguments:
        attributes -- Attributes(data), list of size data_size x n_featurees
        train_index -- Training Indexes, numpy.ndarray of size (train_size, )
        test_index -- Test Indexes, numpy.ndarray of size (test_size, )
        labels -- Labels, list of size data_size
        n_features -- Number of features, int
        f_type -- only used when value is 'sorted_subjects'

    Returns:
        partitioned_data -- Partitioned data, Dictionary of shape:
            {
                'x_train': Training attributes normalized
                    (0 mean and 1 variance)
                'x_test': Test data normalized
                    (0 mean and 1 variance)
                'y_train': Training labels divided by 5
                'y_test': Test labels divided by 5
                'ci_high': 95% Confidence interval high values normalized
                    (0 mean and 1 variance)
                'ci_low': 95% Confidence interval low values normalized
                    (0 mean and 1 variance)
            }
    """
    partitioned_data = partition_data(
        attributes, train_index, test_index, labels, n_features, f_type)

    partitioned_data = normalize_data(partitioned_data)

    return partitioned_data


def substitute_training_data(x_train_all_attributes, y_train):
    """
    Substitute MOS training data with detailed subjetcs training data.

    Arguments:
        x_train_all_attributes -- Training attributes,
                    numpy.ndarray of shape (training_size, n_features)
        y_train -- Training labels, numpy.ndarray of shape
                    (training_size, )

    Returns:
        attributes -- Training attributes,
                    numpy.ndarray of shape (training_size * ~30, n_features)
        labels -- Training labels, numpy.ndarray of shape
                    (training_size * ~30, )
    """
    x_train_all_attributes = pd.DataFrame(x_train_all_attributes)
    y_train = pd.DataFrame(y_train)

    file_name = SORTED_SUBJECTS_DATASET_FILE_NAME

    attributes_tmp = pd.read_csv(file_name)
    attributes_selected_tmp = pd.DataFrame()
    attributes_tmp = attributes_tmp.sample(frac=1).reset_index(drop=True)

    for index, row in x_train_all_attributes.iterrows():
        rows_selected = attributes_tmp.loc[
                (attributes_tmp['VideoFrameRate'] == row[123]) &
                (attributes_tmp['QP'] == row[91]) &
                (attributes_tmp['NR'] == row[124]) &
                (attributes_tmp['VideoPacketLossRate'] ==
                 row[0]) &
                (attributes_tmp['AudioPacketLossRate'] ==
                 row[11])
                ]
        attributes_selected_tmp = attributes_selected_tmp.append(rows_selected)

    attributes_selected_tmp = attributes_selected_tmp.reset_index(drop=True)
    attributes = attributes_selected_tmp.loc[:, :'CILow']
    labels = attributes_selected_tmp.loc[:, 'MOS':]

    return asarray(attributes), asarray(labels)

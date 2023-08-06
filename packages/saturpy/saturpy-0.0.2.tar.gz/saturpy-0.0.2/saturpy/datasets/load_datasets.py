"""
loads different data sets
"""
import os
import pandas as pd


def load_iris():
    """
    load iris data sets
    sepal_length, sepal_width, petal_length, petal_width, species
    150x4
    0=setosa, 1=versicolor, 2=virginica
    :return:
    """
    return pd.read_csv(get_file_path('data/iris.csv'))


def get_file_path(file_to_load):
    """
    append the path file path into data path
    :param file_to_load:
    :return:
    """
    # TODO manage proper data set loading
    return os.path.join(os.getcwd(), 'saturpy/datasets', file_to_load)


class DataSet:
    """
    load dataset into class
    """
    def __init__(self):
        self.data = []
        self.feature = []
        self.targets = []

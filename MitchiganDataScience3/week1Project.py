#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 16:53:25 2017

"""


import pandas as pd

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

cancer = load_breast_cancer()


def answer_one():
    # import the cancer dataset into a pandas DataFrame
    columns = ['mean radius', 'mean texture', 'mean perimeter', 'mean area',
     'mean smoothness', 'mean compactness', 'mean concavity',
     'mean concave points', 'mean symmetry', 'mean fractal dimension',
     'radius error', 'texture error', 'perimeter error', 'area error',
     'smoothness error', 'compactness error', 'concavity error',
     'concave points error', 'symmetry error', 'fractal dimension error',
     'worst radius', 'worst texture', 'worst perimeter', 'worst area',
     'worst smoothness', 'worst compactness', 'worst concavity',
     'worst concave points', 'worst symmetry', 'worst fractal dimension']

    df = pd.DataFrame(data=cancer.data, columns=columns, index=range(569))
    df['target'] = cancer.target
    return df


def answer_two():
    # malignant = 0, benign = 1  summarize quantity of each
    df = answer_one()
    n = len(df)
    benign = df['target'].sum()
    malignant = n - benign
    
    answer_dict = {'malignant': malignant, 'benign': benign}
    return pd.Series(data=answer_dict)


def answer_three():
    # split data into fields (X) and goal (y)
    df = answer_one()

    X = df.iloc[:, :-1]
    y = df['target']
    return (X, y)


def answer_four():
    # split the data into training and testing portions
    X, y = answer_three()

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    return (X_train, X_test, y_train, y_test)


def answer_five():
    # set up K-nearest neighbors and train on data
    X_train, X_test, y_train, y_test = answer_four()

    knn = KNeighborsClassifier(n_neighbors=1)
    return knn.fit(X_train, y_train)


def answer_six():
    # predict cancer status of new case with mean values for all fields
    df = answer_one()
    means = df.mean()[:-1].values.reshape(1, -1)

    return answer_five().predict(means)


def answer_seven():
    # predict cancer status of our test dataset
    X_train, X_test, y_train, y_test = answer_four()

    return answer_five().predict(X_test)


def answer_eight():
    # calculate the accuracy of our model on the testing dataset
    X_train, X_test, y_train, y_test = answer_four()

    return answer_five().score(X_test, y_test)


# END

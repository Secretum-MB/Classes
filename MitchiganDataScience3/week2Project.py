#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 20:11:29 2017

"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


np.random.seed(0)
n = 15
x = np.linspace(0,10,n) + np.random.randn(n)/5
y = np.sin(x)+x/6 + np.random.randn(n)/10


X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0)


def answer_one():
    # train polynomial linear regression model and retrieve predictions on test
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures

    res = np.zeros((4,100))
    for i in [1, 3, 6, 9]:
        # create a polynomial feature object
        poly = PolynomialFeatures(degree=i)

        # reshape x_train and convert it to polynomial feature
        x_train_poly = poly.fit_transform(X_train.reshape((11,1)))

        # define and fit linear regression model
        linreg = LinearRegression().fit(x_train_poly, y_train)

        # create x values to create predictions for and transform to feature
        test_x = np.linspace(0,10,100).reshape(-1,1)
        x_test_poly = poly.transform(test_x)

        # create predictions and store in numpy array
        y_predict = linreg.predict(x_test_poly)
        res[i,:] = y_predict
        return res


def answer_two():
    # compare the score of polynomial linear regression model with differing
    # polynomial degrees.
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.metrics.regression import r2_score

    r2_train, r2_test = [], []
    for i in range(0,10):
        # create a polynomial feature object
        poly = PolynomialFeatures(degree=i)

        # reshape x_train and convert it to polynomial feature
        x_train_poly = poly.fit_transform(X_train.reshape((11,1)))

        # define and fit linear regression model
        linreg = LinearRegression().fit(x_train_poly, y_train)

        # create predictions for testing data
        x_test_poly = poly.transform(X_test.reshape((4,1)))
        y_predict_test = linreg.predict(x_test_poly)

        # create predictions for training data
        x_train_poly = poly.transform(X_train.reshape((11,1)))
        y_predict_train = linreg.predict(x_train_poly)

        # calculate r^2 for model and add to list
        r2_train.append(r2_score(y_train, y_predict_train))
        r2_test.append(r2_score(y_test, y_predict_test))
    return tuple(np.array((r2_train, r2_test)))


def answer_three():
    # returning degree that is underfitting, overfitting, good fit
    return (0, 9, 7)


def answer_four():
    # Compare the score of lasso regression vs linear regression
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.linear_model import Lasso, LinearRegression
    from sklearn.metrics.regression import r2_score

    # create a polynomial feature object
    poly = PolynomialFeatures(degree=12)

    # reshape x_train and convert it to polynomial feature
    x_train_poly = poly.fit_transform(X_train.reshape((11,1)))

    # define and fit linear regression model
    linreg = LinearRegression().fit(x_train_poly, y_train)

    # create predictions for testing data
    x_test_poly = poly.transform(X_test.reshape((4,1)))
    y_predict_test = linreg.predict(x_test_poly)

    # score of lr
    lr_score = r2_score(y_test, y_predict_test)

    #define and fit lasso regression model
    linlasso = Lasso(0.01, max_iter = 10000).fit(x_train_poly, y_train)

    # create predictions for test data
    y_predict_test = linlasso.predict(x_test_poly)

    # score of lasso lr
    lasso_score = r2_score(y_test, y_predict_test)

    return (lr_score, lasso_score)


# Part 2 of Project

# import mushroom dataset, convert catagorical data to binary indicator values
mush_df = pd.read_csv('mushrooms.csv')
mush_df2 = pd.get_dummies(mush_df)

X_mush = mush_df2.iloc[:, 2:]
y_mush = mush_df2.iloc[:, 1]

# split dataset into training and testing
X_train2, X_test2, y_train2, y_test2 = train_test_split(X_mush, y_mush, random_state=0)

# this creates a subset of the data that will be used in Q 6 and 7 (for time reasons)
X_subset = X_test2
y_subset = y_test2


def answer_five():
    # retrieve the 5 most significant features
    from sklearn.tree import DecisionTreeClassifier

    # create tree object and
    tree = DecisionTreeClassifier().fit(X_train2, y_train2)
    features = tree.feature_importances_.argsort()[-5:][::-1]

    # map index of features to column header
    results = []
    for i in features:
        results.append(X_train2.columns[i])
    return results


def answer_six():
    # explore classifier average accuracy across 6 different gammas using a
    # validation curve that creates 3 models per gamma.
    from sklearn.svm import SVC
    from sklearn.model_selection import validation_curve

    # creating a Support vector Classifier
    svc = SVC(kernel='rbf', C=1.0, random_state=0)

    # calculate model scores of support vector using validation curve, varying gamma
    train, test = validation_curve(svc, X_subset, y_subset, 'gamma',
                                   np.logspace(-4,1,6), scoring='accuracy')
    training_scores = []
    testing_scores = []
    for gamma_run in train:
        training_scores.append(np.mean(gamma_run))

    for gamma_run in test:
        testing_scores.append(np.mean(gamma_run))

    return (training_scores, testing_scores)


def answer_seven():
    # return from above the gamma values in that map as following:
    # (underfitting, overfitting, good_generalization)
    all_gammas = np.logspace(-4,1,6)

    # From reviewing output of question 6, we know:
    # (first gamma, last gamma, third)
    return (all_gammas[0], all_gammas[5], all_gammas[2])


# END

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 14:43:51 2017

"""
from sklearn.model_selection import test_train_split
from sklearn.neighbors import KNeighborsClassifier

import numpy as np
import pandas as pd
#import scipy
import matplotlib.pyplot as plt


# Supervised Machine Learning Application using K-nearest neighbors algorithm

# 1. Place data in pandas Dataframe, clean up data if necessary

# 2. Break data up into train and test data after breaking data up into X, y

X = fruits[['mass', 'width', 'height']]
y = fruits['fruit_label']

X_train, X_test, y_train, y_test = test_train_split.train_test_split(X, y)

# 3. Create classifier object

knn = KNeighborsClassifier.KNeighborsClassifier(n_neighbors=5)

# 4. Train the classifier

knn.fit(X_train, y_train)

# 5. Determine the accuracy of classifier

knn.score(X_test, y_test)

# 6. Use classifier to predict classification of new data

prediction = knn.predict([[20, 4.3, 6.0]])  # mass, width, height

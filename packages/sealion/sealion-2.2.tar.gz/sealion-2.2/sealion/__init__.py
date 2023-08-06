"""
SeaLion is a simple machine learning and data science library.

=============================================================

Designed with beginners in mind, it has rich documentation via Pydoc and algorithms that span from the most basic
to more modern approaches. It is meant to help beginners navigate it all, and the documentation not only explains t
he models and their respective functions but also what they are and when to use them. Emphasis was also put on creating
new functions to make it interesting for those who are just getting started and seasoned ml-engineers alike.

I hope you enjoy it!
- Anish Lakkapragada 2021
"""

from sealion.DimensionalityReduction import tSNE, PCA
from sealion.utils import one_hot, revert_one_hot, revert_softmax, confusion_matrix
from sealion.ensemble_learning import RandomForest, EnsembleClassifier
from sealion.unsupervised_clustering import KMeans, DBSCAN
from sealion.regression import LinearRegression, LogisticRegression, SoftmaxRegression, RidgeRegression, LassoRegression, ElasticNet, PolynomialRegression, ExponentialRegression
from sealion.nearest_neighbors import KNearestNeighbors

from sealion.neural_networks.optimizers import GD, Momentum, SGD, AdaGrad, RMSProp, Adam
from sealion.neural_networks.layers import Dense, Flatten, Dropout, ReLU, ELU, SELU, LeakyReLU, Sigmoid, Tanh, Swish
from sealion.neural_networks.models import NeuralNetwork, NeuralNetwork_MapReduce
from sealion.neural_networks.loss import CrossEntropy, MSE

from sealion import cython_models

__all__ = ['neural_networks', 'decision_trees', 'DimensionalityReduction', 'ensemble_learning', 'regression', 'unsupervised_clustering', 'utils', 'nearest_neighbors', 'cython_models']
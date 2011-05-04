#-*- coding:utf-8 -*-

__author__ = 'caracioL@gmail.com'

import unittest
import sys
from math import sqrt
import pickle
import pylab as pl

#Put the path of the root folder of crab framework. E.g.: C://crab/crab
sys.path.append('/Users/marcelcaraciolo/Desktop/crab/crab/crab')

from models.datamodel import *
from recommender.recommender import  SlopeOneRecommender
from recommender.utils import DiffStorage
from evaluation.statistics import *

#Load the dataset
input = open('model.pk1', 'rb')
model = pickle.load(input)
model = DictDataModel(model)

#Instantiate the Evaluator
evaluator = RMSRecommenderEvaluator()
#Instantiate the Slope One Recommender
recommender = SlopeOneRecommender(model,True,False,False)

#Calculate the Root Mean Squared Error
rmse = evaluator.evaluate(recommender,model,0.7,1.0)

#Instantiate the IR Stats Recommender Evaluator
evaluator = IRStatsRecommenderEvaluator()

#Calculate the Precision, Recall and F1Score
result = evaluator.evaluate(recommender,model,25,1.0)

#1.04078332386 0.17222222222222 0.1722222222222 0.17222222222222
print rmse, result['precision'], result['recall'], result['f1Score']


#For plotting the graph.
import scipy as sc
import pylab as pl
import recallPrecision as rp
#Fetched these data manually (tuple - Precision, Recall) 
prs = [(0.0834,0.0856), (0.17222,0.172222), (0.17222,0.17222),(0.21023,0.21344)] # precision recall point list
labels = ["size=10", "size=20", "size=30", "size=40"] # labels for the points
rp.plotPrecisionRecallDiagram("Precision - Recall Diagram", prs, labels)
pl.show()




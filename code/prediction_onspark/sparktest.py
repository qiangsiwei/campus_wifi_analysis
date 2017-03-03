import numpy as np
from pyspark import SparkContext
import pyspark.mllib.classification as cl

sc = SparkContext('local', 'Predict')
data = np.array([0.0, 0.0, 1.0, 1.0, 1.0, 2.0, 1.0, 3.0]).reshape(4,2)
svm = cl.SVMWithSGD.train(sc.parallelize(data))
svm.predict(np.array([1.0]))
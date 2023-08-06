from pyspark.ml.linalg import Vectors
import numpy as np


def initCenteroid(rdd, nCenteroid, seed):
    return rdd.takeSample(False, nCenteroid, seed)


def calculateDistance(numCenteroid):
    def calculate(rdd):
        return Vectors.dense([rdd.squared_distance(center) for center in numCenteroid])

    return calculate


def calculateDissim(gamma, catCenteroid):
    def calculate(rdd):
        return Vectors.dense([gamma * np.sum(rdd != center) for center in catCenteroid])

    return calculate


def getMode(array):
    return np.apply_along_axis(
        lambda x: np.float64(np.bincount(x).argmax()), axis=0, arr=array
    )


def updateNumCenteroid(numRDD, cluster):
    return (
        cluster.zip(numRDD)
        .groupByKey()
        .mapValues(lambda x: sum(x) / len(x))
        .map(lambda x: x[1])
        .collect()
    )


def updateCatCenteroid(catRDD, cluster):
    return (
        cluster.zip(catRDD)
        .groupByKey()
        .mapValues(list)
        .map(lambda row: getMode(row[1]))
        .collect()
    )


def predict(numRDD, catRDD, gamma, numCenteroid, catCenteroid):
    squared_distance = numRDD.map(calculateDistance(numCenteroid))
    dissim_distance = catRDD.map(calculateDissim(gamma, catCenteroid))
    distance = squared_distance.zip(dissim_distance).map(lambda row: sum(row))
    cluster = distance.map(lambda vect: vect.argmin())
    return distance, cluster


def mergeDict(xDict, yDict):
    xDict.update(yDict)
    return xDict

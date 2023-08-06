import numpy as np
from pyspark import keyword_only
from pyspark.sql import Row
from pyspark.ml.util import DefaultParamsReadable, DefaultParamsWritable
from pyspark.ml.pipeline import Estimator, Model
from pyspark.ml.param.shared import Param, Params, TypeConverters, HasPredictionCol
from .utils import (
    initCenteroid,
    predict,
    mergeDict,
    updateCatCenteroid,
    updateNumCenteroid,
)


class HasNCenteroid(Params):

    nCenteroid = Param(
        parent=Params._dummy(),
        name="nCenteroid",
        doc="nCenteroid",
        typeConverter=TypeConverters.toInt,
    )

    def __init__(self):
        super(HasNCenteroid, self).__init__()

    def setNCenteroid(self, value):
        return self._set(nCenteroid=value)

    def getNCenteroid(self):
        return self.getOrDefault(self.nCenteroid)


class HasMaxIter(Params):

    maxIter = Param(
        parent=Params._dummy(),
        name="maxIter",
        doc="maxIter",
        typeConverter=TypeConverters.toInt,
    )

    def __init__(self):
        super(HasMaxIter, self).__init__()

    def setMaxIter(self, value):
        return self._set(maxIter=value)

    def getMaxIter(self):
        return self.getOrDefault(self.maxIter)


class HasGamma(Params):

    gamma = Param(
        parent=Params._dummy(),
        name="gamma",
        doc="gamma",
        typeConverter=TypeConverters.toFloat,
    )

    def __init__(self):
        super(HasGamma, self).__init__()

    def setGamma(self, value):
        return self._set(gamma=value)

    def getGamma(self):
        return self.getOrDefault(self.gamma)


class HasCatCol(Params):

    catCol = Param(
        parent=Params._dummy(),
        name="catCol",
        doc="catCol",
        typeConverter=TypeConverters.toString,
    )

    def __init__(self):
        super(HasCatCol, self).__init__()

    def setCatCol(self, value):
        return self._set(catCol=value)

    def getCatCol(self):
        return self.getOrDefault(self.catCol)


class HasNumCol(Params):

    numCol = Param(
        parent=Params._dummy(),
        name="numCol",
        doc="numCol",
        typeConverter=TypeConverters.toString,
    )

    def __init__(self):
        super(HasNumCol, self).__init__()

    def setNumCol(self, value):
        return self._set(numCol=value)

    def getNumCol(self):
        return self.getOrDefault(self.numCol)


class HasSeed(Params):

    seed = Param(
        parent=Params._dummy(),
        name="seed",
        doc="seed",
        typeConverter=TypeConverters.toInt,
    )

    def __init__(self):
        super(HasSeed, self).__init__()

    def setSeed(self, value):
        return self._set(seed=value)

    def getSeed(self):
        return self.getOrDefault(self.seed)


class HasNumCenteroid(Params):

    numCenteroid = Param(
        parent=Params._dummy(),
        name="numCenteroid",
        doc="numCenteroid",
        typeConverter=TypeConverters.toList,
    )

    def __init__(self):
        super(HasNumCenteroid, self).__init__()

    def setNumCenteroid(self, value):
        return self._set(numCenteroid=value)

    def getNumCenteroid(self):
        return self.getOrDefault(self.numCenteroid)


class HasCatCenteroid(Params):

    catCenteroid = Param(
        parent=Params._dummy(),
        name="catCenteroid",
        doc="catCenteroid",
        typeConverter=TypeConverters.toList,
    )

    def __init__(self):
        super(HasCatCenteroid, self).__init__()

    def setCatCenteroid(self, value):
        return self._set(catCenteroid=value)

    def getCatCenteroid(self):
        return self.getOrDefault(self.catCenteroid)


class HasDistance(Params):

    distance = Param(
        parent=Params._dummy(),
        name="distance",
        doc="distance",
        typeConverter=TypeConverters.toList,
    )

    def __init__(self):
        super(HasDistance, self).__init__()

    def setDistance(self, value):
        return self._set(distance=value)

    def getDistance(self):
        return self.getOrDefault(self.distance)


class KPrototypes(
    Estimator,
    HasNumCol,
    HasCatCol,
    HasPredictionCol,
    HasNCenteroid,
    HasGamma,
    HasMaxIter,
    HasSeed,
    DefaultParamsReadable,
    DefaultParamsWritable,
):
    @keyword_only
    def __init__(
        self,
        numCol=None,
        catCol=None,
        predictionCol=None,
        nCenteroid=None,
        gamma=0.5,
        maxIter=100,
        seed=0,
    ):
        super(KPrototypes, self).__init__()
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

    def setPredictionCol(self, value):
        return self._set(predictionCol=value)

    def setParams(
        self,
        numCol=None,
        catCol=None,
        predictionCol=None,
        nCenteroid=None,
        gamma=0.5,
        maxIter=100,
        seed=0,
    ):
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def _fit(self, dataset):
        numRDD = dataset.select(self.getNumCol()).rdd.flatMap(list)
        catRDD = (
            dataset.select(self.getCatCol())
            .rdd.flatMap(list)
            .map(lambda row: np.int64(row))
        )
        numCenteroid = initCenteroid(
            rdd=numRDD, nCenteroid=self.getNCenteroid(), seed=self.getSeed()
        )
        catCenteroid = initCenteroid(
            rdd=catRDD, nCenteroid=self.getNCenteroid(), seed=self.getSeed()
        )

        for i in range(self.getMaxIter()):
            distance, cluster = predict(
                numRDD=numRDD,
                catRDD=catRDD,
                numCenteroid=numCenteroid,
                catCenteroid=catCenteroid,
                gamma=self.getGamma(),
            )

            numCenteroid = updateNumCenteroid(numRDD=numRDD, cluster=cluster)
            catCenteroid = updateCatCenteroid(catRDD=catRDD, cluster=cluster)

        return KPrototypesModel(
            numCol=self.getNumCol(),
            catCol=self.getCatCol(),
            predictionCol=self.getPredictionCol(),
            gamma=self.getGamma(),
            numCenteroid=numCenteroid,
            catCenteroid=catCenteroid,
            distance=distance.collect(),
        )


class KPrototypesModel(
    Model,
    HasNumCol,
    HasCatCol,
    HasPredictionCol,
    HasGamma,
    HasDistance,
    HasNumCenteroid,
    HasCatCenteroid,
    DefaultParamsReadable,
    DefaultParamsWritable,
):
    @keyword_only
    def __init__(
        self,
        numCol=None,
        catCol=None,
        predictionCol=None,
        gamma=None,
        numCenteroid=None,
        catCenteroid=None,
        distance=None,
    ):
        super(KPrototypesModel, self).__init__()
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

    def setParams(
        self,
        numCol=None,
        catCol=None,
        predictionCol=None,
        gamma=None,
        numCenteroid=None,
        catCenteroid=None,
        distance=None,
    ):
        kwargs = self._input_kwargs
        return self._set(**kwargs)

    def _transform(self, dataset):
        numRDD = dataset.select(self.getNumCol()).rdd.flatMap(list)
        catRDD = (
            dataset.select(self.getCatCol())
            .rdd.flatMap(list)
            .map(lambda row: np.int64(row))
        )
        _, cluster = predict(
            numRDD=numRDD,
            catRDD=catRDD,
            numCenteroid=self.getNumCenteroid(),
            catCenteroid=self.getCatCenteroid(),
            gamma=self.getGamma(),
        )
        return (
            dataset.rdd.zip(cluster.map(lambda row: int(row)))
            .map(
                lambda row: Row(
                    **mergeDict(row[0].asDict(), {self.getPredictionCol(): row[1]})
                )
            )
            .toDF()
        )

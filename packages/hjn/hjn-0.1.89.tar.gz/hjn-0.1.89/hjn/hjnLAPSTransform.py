# -*- coding:utf-8 -*-
# Author:hujunnan

import numpy as np


class LAPSTransfrom():
    def __init__(self,p,lonMat, latMat,env,step=0.03):
        xMat, yMat = p(lonMat, latMat)
        x0 = np.min(xMat)
        y0 = np.max(yMat)
        lat0 = env.n
        lat1 = env.s
        lon0 = env.w
        lon1 = env.e
        self.step = step
        self.rangeLat = int(np.round(((lat0 - lat1) / step), 0)) + 1
        self.rangeLon = int(np.round(((lon1 - lon0) / step), 0)) + 1
        self.latArr = np.linspace(lat0, lat1, self.rangeLat)
        self.lonArr = np.linspace(lon0, lon1, self.rangeLon)
        latMatCHN = np.repeat([self.latArr], self.rangeLon, axis=0).T
        lonMatCHN = np.repeat([self.lonArr], self.rangeLat, axis=0)
        latMatCHNArr = latMatCHN.reshape(-1)
        lonMatCHNArr = lonMatCHN.reshape(-1)
        x, y = p(lonMatCHNArr, latMatCHNArr)
        self.latIdx = ((y0 - y) / 3000 + 0.5).astype(int)
        self.lonIdx = ((x - x0) / 3000 + 0.5).astype(int)
        self.latMaskValid = np.logical_or(self.latIdx < 0, self.latIdx >= latMat.shape[0])
        self.lonMaskValid = np.logical_or(self.lonIdx < 0, self.lonIdx >= latMat.shape[1])
        self.latIdx[self.latMaskValid] = 0
        self.lonIdx[self.lonMaskValid] = 0

    def LambertToLatLon(self,t):
        lambertMat = t[self.latIdx, self.lonIdx]
        lambertMat = lambertMat.reshape([self.rangeLat, self.rangeLon])
        lambertMat[self.latMaskValid.reshape([self.rangeLat, self.rangeLon])] = np.nan
        lambertMat[self.lonMaskValid.reshape([self.rangeLat, self.rangeLon])] = np.nan
        return lambertMat


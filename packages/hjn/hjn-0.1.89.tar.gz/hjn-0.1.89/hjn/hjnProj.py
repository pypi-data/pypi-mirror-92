import numpy as np
from hjn.mkNCHJN import envelope

class FY4Proj():
    def __init__(self,lonD=104.7,resolution=4000):

        self.ea=6378.137
        self.eb=6356.7523
        self.h=42164
        self.lambdaD=np.radians(lonD)        

        OFF={500:10991.5,1000:5495.5,2000:2747.5,4000:1373.5}
        FAC={500:81865099,1000:40932549,2000:20466274,4000:10233137}       
        
        self.COFF=OFF[resolution]
        self.LOFF=OFF[resolution]
        self.CFAC=FAC[resolution]
        self.LFAC=FAC[resolution]

    def transform(self,latD,lonDe):
        lat=np.radians(latD)
        lon=np.radians(lonDe)
        ba2=np.square(self.eb/self.ea)
        phie=np.arctan(ba2*np.tan(lat))
        diffLon0=lon-self.lambdaD
        re=self.eb/np.sqrt(1-(1-ba2)*np.square(np.cos(phie)))

        r1=self.h-re*np.cos(phie)*np.cos(diffLon0)
        r2= -re*np.cos(phie)*np.sin(diffLon0)
        r3=re*np.sin(phie)
        rn=np.sqrt(np.square(r1)+np.square(r2)+np.square(r3))


        x= np.degrees(np.arctan(-r2/r1))
        y= np.degrees(np.arcsin(-r3/rn))

        c=(self.COFF+x*np.power(float(2),-16)*self.CFAC -0.5).astype(np.int32)
        l=(self.LOFF+y*np.power(float(2),-16)*self.LFAC -0.5).astype(np.int32)
        return (l,c)
    
    def transforMat(self,ltc,step,SNCmat):
        _,_,latMat,lonMat = getLatlonMat(ltc,step)
        (l,c)=self.transform(latMat,lonMat)
        snclatlon=SNCmat[l,c]
        return snclatlon

class H8Proj():
    def __init__(self, lonD=140.7, resolution=2000):
        self.ea = 6378.137
        self.eb = 6356.7523
        self.h = 42165.32745491
        self.lambdaD = np.radians(lonD)

        OFF = {500: 11000.5, 1000: 5500.5 , 2000: 2750.5}
        FAC = {500: 81865099, 1000: 40932549, 2000: 20466275}

        self.COFF = OFF[resolution]
        self.LOFF = OFF[resolution]
        self.CFAC = FAC[resolution]
        self.LFAC = FAC[resolution]


    def transform(self,latD, lonDe):
        lat = np.radians(latD)
        lon = np.radians(lonDe)
        ba2 = np.square(self.eb / self.ea)
        phie = np.arctan(ba2 * np.tan(lat))
        diffLon0 = lon - self.lambdaD
        re = self.eb / np.sqrt(1 - (1 - ba2) * np.square(np.cos(phie)))

        r1 = self.h - re * np.cos(phie) * np.cos(diffLon0)
        r2 = -re * np.cos(phie) * np.sin(diffLon0)
        r3 = re * np.sin(phie)
        rn = np.sqrt(np.square(r1) + np.square(r2) + np.square(r3))

        x = np.degrees(np.arctan(-r2 / r1))
        y = np.degrees(np.arcsin(-r3 / rn))

        c = (self.COFF + x * np.power(float(2), -16) * self.CFAC - 0.5).astype(np.int32)
        l = (self.LOFF + y * np.power(float(2), -16) * self.LFAC - 0.5).astype(np.int32)
        return (l, c)

    def transforMat(self,ltc,step,SNCmat,loff):
        _,_,latMat,lonMat = getLatlonMat(ltc,step)
        (l,c)=self.transform(latMat,lonMat)
        snclatlon=SNCmat[l-int(loff),c]
        return snclatlon


def getLatlonMat(ltc,step):
    latArr = np.linspace(ltc.n, ltc.s, int((ltc.n - ltc.s) // step) + 2)
    lonArr = np.linspace(ltc.w, ltc.e, int((ltc.e - ltc.w) // step) + 2)
    latMat = np.dot(latArr.reshape(-1, 1), np.ones([1, len(lonArr)]))
    lonMat = np.dot(np.ones([len(latArr), 1]), np.expand_dims(lonArr, axis=0))
    return latArr,lonArr,latMat,lonMat

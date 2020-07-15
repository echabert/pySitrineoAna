import math
import os

class dEdxCalculator:
    """
    lenght are expressed in microns
    charge in e-
    assumes that the charge density distribution follows a gaussian distribution with a width = sigma
    the cluser size thus follows the function (2xPIxSigma^2)/(pitch^2) x log ( Qtot / (2xPIxThreshold x Sigma^2))
    pid: 11 (electrons), 2212 (protons)
    material supported: Al, Si, Air, Kapton
    dEdx calculation based on tabulated values
      linear interpolation are done in the considered range ([0.01-3 MeV] for e-, [0.1-30 MeV] for proton)
      improvement to be done: spline cubic
    """
    def __init__(self, filename=""):
        self.pitch = 20.7
        self.thickness = 15
        self.sigma = 8.26
        self.sigma_err = 0.01
        self.threshold = 12 # expressed in sigma
        self.th2e = 188./12 # factor to convert a sigma into electrons
        self.Eg = 3.6 # energy in eV for pair creation
        self.material = "Si"
        self.rho = 2.7 # volumic mass of Silicon [g/cm2]
        self.dEdxTable_e = []
        self.dEdxTable_p = []
        if filename != "":
            self.Config(filename)

    def Config(self,filename):
        """
            Load the values from a file
        """
        #print("Cconfig")
        with open(filename) as ifile:
            for line in ifile:
                print(line)
                varname =  line.strip().split("#")[0].split("=")[0]
                value = line.strip().split("#")[0].split("=")[1]
                print(varname,value)
                #print(self.__dict__.keys())
                for key in self.__dict__.keys():
                    #print(key, varname)
                    #print("there",key,varname)
                    if str(key.strip()) == str(varname.strip()):
                        if str(key.strip())=="material":
                            self.__dict__[key] = value
                        else:
                            self.__dict__[key] = float(value)
                print(os.getcwd())
                if varname.strip()== "fname_dEdxTable_electron":
                    self.LoadDeDxTable(value.strip(), 11)
                if varname.strip() == "fname_dEdxTable_proton":
                    self.LoadDeDxTable(value.strip(), 2212)
                
    def LoadDeDxTable(self,filename, pid):
        print("loading tbale")
        with open(filename) as ifile:
            for line in ifile:
                if pid == 1: self.dEdxTable_e.append([float(line.split()[0]),float(line.split()[1])])
                if pid == 2212: self.dEdxTable_e.append([float(line.split()[0]),float(line.split()[1])])
        print(self.dEdxTable_e)

    def LoadFitParameters(self,a,b): 
        """ assumes clusterSize = a x log (b/T)
        """
        self.sigma = math.sqrt(a*pow(pitch,2)/(2*math.pi))

    def GetdEdX(self,clusterSize):
        """
         Compute dEdX based on the cluster size
         Results expressed in MeV.cm2/g
        """
        return self.GetEloss(clusterSize)/(self.pitch*100/self.rho)

    def GetCharge(self,clusterSize):
        return math.exp(clusterSize*pow(self.pitch,2)/(2*math.pi*pow(self.sigma,2))) * 2*math.pi*self.threshold*self.th2e*pow(self.sigma,2)

    def GetEloss(self,clusterSize):
        return self.GetCharge(clusterSize)*self.Eg

    def GetMomenta(self, clusterSize, pid = 11):
        if pid == 11: return self.GetMomenta(GetdEdX(clusterSize), dEdxTable_e)
        if pid == 2212: return self.GetMomenta(GetdEdX(clusterSize), dEdxTable_p)

    """ For internal use """
    def GetMomenta(self, clusterSize, pid):
        """
         Perform a linear interpolation
         Could be improved by 2nd order pol interpolation
        """
        dedx = self.GetdEdX(clusterSize)
        table = []
        if pid == 11:
            table = self.dEdxTable_e
        if pid == 2212:
            table = self.dEdxTable_p
        print(table)
        for index in range(len(table)-1):
            if dedx>table[index][1] and dedx<table[index+1][1]:
                return self.LinearInterpolation(dedx,table[index][0],table[index][1],table[index+1][0],table[index+1][1])
        return -1 # if it fails

    def LinearInterpolation(self,x0,x1,y1,x2,y2):
        a = (y2-y1)/(x2-x1)
        b = y1-a*x1
        return a*x0+b
   
    #def CubicSpline(self, x0, x1, y1, x2, y2):
    #    tx = (x0-x1)/(x2-x1)
    #    a = k1*(x2-x1)-(y2-y1)
    #    b = -k2*(x2-x1)+(y2-y1)


    def __str__(self):
        output="dEdX calculator:\n"
        output+="Pitch = "+str(self.pitch)+ " um \t thickness = "+str(self.thickness)+" um \n"
        output+="Material = "+self.material+"\t rho = "+str(self.rho)+" Eg = "+str(self.Eg)+" e\n"
        output+="Sigma (spatial) = "+str(self.sigma)+" +/- "+str(self.sigma_err)+"\n"
        output+="Threshold (def) = "+str(self.threshold)+" sigma where sigma = "+str(self.th2e)+" e-\n"
        return output

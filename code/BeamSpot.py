import ROOT
from ROOT import gROOT,TEllipse, TH1F, TH2F, TCanvas, TF1, TFile, TGraph, gApplication, TLegend
import math



################################################
## Class BeamSpot
################################################

class BeamSpot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.xErr = 0
        self.yErr = 0
        self.xwidth = 0
        self.ywidth = 0
        self.xwidthErr = 0
        self.ywidthErr = 0
    
    def __init__(self,X=0,Y=0,XErr=0,YErr=0,XWidth=0,YWidth=0,XWidthErr=0,YWidthErr=0):
        self.x = X
        self.y = Y
        self.xErr = XErr
        self.yErr = YErr
        self.xwidth = XWidth
        self.ywidth = YWidth
        self.xwidthErr = XWidthErr
        self.ywidthErr = YWidthErr

    def Distance(self,beam):
        math.sqrt((self.x-beam.x)*(self.x-beam.x)+(self.y-beam.y)*(self.y-beam.y))
    
    #return x-shift and the associated error
    def XShift(self,beam):
        return beam.x-self.x,math.sqrt(beam.xErr*beam.xErr+self.xErr*self.xErr)

    #return y-shift and the associated error
    def YShift(self,beam):
        return beam.y-self.y,math.sqrt(beam.yErr*beam.yErr+self.yErr*self.yErr)

    #multiple scattering: additional width increase
    def xMSWidth(self,beam):
        res = 0
        if beam.xwidth>self.xwidth: res = math.sqrt(beam.xwidth*beam.xwidth-self.xwidth*self.xwidth)
        else: res = math.sqrt(-beam.xwidth*beam.xwidth+self.xwidth*self.xwidth)
        error = math.sqrt(beam.xwidthErr*beam.xwidthErr+self.xwidthErr*self.xwidthErr)
        return res,error
    
    #multiple scattering: additional width increase
    def yMSWidth(self,beam):
        res = 0
        if beam.ywidth>self.ywidth: res = math.sqrt(beam.ywidth*beam.ywidth-self.ywidth*self.ywidth)
        else: res = math.sqrt(self.ywidth*self.ywidth-beam.ywidth*beam.ywidth)
        error = math.sqrt(beam.ywidthErr*beam.ywidthErr+self.ywidthErr*self.ywidthErr)
        return res, error

    def GetStr(self,withErr=False):
        output = "Center ( %0.1f"%self.x
        if withErr: output+=" +/- %0.1f"%self.xErr
        output+=" , %0.1f"%self.y
        if withErr: output+=" +/- %0.1f"%self.yErr
        output+=" )"
        output+=" Widths ( %0.1f"%self.xwidth
        if withErr: output+=" +/- %0.1f"%self.xwidthErr
        output+=" , %0.1f"%self.ywidth
        if withErr: output+=" +/- %0.1f"%self.ywidthErr
        output+=" )"
        return output

    def GetCSVHead(self):
        output = "x,xErr,y,yErr,xwidth,xwidthErr,ywidth,ywidthErr"
        return output

    def GetCSV(self):
        output = "%0.1f"%self.x
        output+=",%0.1f"%self.xErr
        output+=",%0.1f"%self.y
        output+=",%0.1f"%self.yErr
        output+=",%0.1f"%self.xwidth
        output+=",%0.1f"%self.xwidthErr
        output+=",%0.1f"%self.ywidth
        output+=",%0.1f"%self.ywidthErr
        return output

    def LoadCSV(self, info):
        if len(info.split(','))<8:
            return None
        values = info.split(',')
        self.x = float(values[0])
        self.xErr = float(values[1])
        self.y = float(values[2])
        self.yErr = float(values[3])
        self.xwidth = float(values[4])
        self.ywidthErr = float(values[5])
        self.ywidth = float(values[6])
        self.xwidthErr = float(values[7])

    def Print(self,withErr=False):
        print(GetStr(withErr))

    def GetEllipseCenter(self,color=1,width=1,linestyle=1,fillstyle=0):
        el = TEllipse(self.x,self.y,self.xErr,self.yErr)
        el.SetLineColor(color)
        el.SetFillColor(color)
        el.SetLineWidth(width)
        el.SetLineStyle(linestyle)
        el.SetFillStyle(fillstyle)
        return el



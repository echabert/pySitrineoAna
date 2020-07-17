import ROOT
from ROOT import gROOT, TH1F, TCanvas, TF1, TFile, TGraph, TGraphErrors, gApplication, TLegend
ROOT.gROOT.Reset()
#app = ROOT.gApplication
import math


#########################################
# Configuration
#########################################

dir = "/Users/echabert/Work/taf/Results/"
filenamebase = "sitrineo_run"
#list the runs: run number, threholsd [in sigmas]
#Threhsold scans
#runs = [(6,5),(8,8),(9,10),(10,12),(14,15),(11,20),(12,25),(13,30)]
#runs = [(66,12),(67,12),(69,12),(70,12),(72,12)]
#intensity runs
runs = [(20,12),(24,12),(66,12),(67,12),(69,12)]
#runs = [(6,5),(8,8)]
plotname = "hhitpixpl"
oufilename = "totoDictionnary.dat"
write = True
logscale = False


#########################################
# Code
#########################################
canvas = TCanvas()
canvas.cd()
if logscale:
    canvas.SetLogy()

peakDict = {}
for channel in range(1,5):
   for run in runs:
      print("Run",run,"channel",channel)
      ifile = TFile(dir+str(run[0])+"/"+filenamebase+str(run[0])+".root")
      plot = TH1F(ifile.Get(plotname+str(channel)))
      plot.GetXaxis().SetRangeUser(0,50)
      plot.Draw()
      canvas.Update()
      canvas.Modified()
      canvas.WaitPrimitive()
      if write:
        x0=input("x0 [enter -1 if not found]\n")
        x1=input("x1 [enter -1 if not found]\n")
        x2=input("x2 [enter -1 if not found]\n")
        x3=input("x3 [enter -1 if not found]\n")
        peakDict[(run[0],channel)] = [x0,x1,x2,x3]


#########################################
# Report
#########################################
if write:
  print(peakDict)
  with open(ofilename,"w") as ofile:
    for key, value in peakDict.items():
        message = str(key)+" "+str(value[0])+" "+str(value[1])+" "+str(value[2])+"\n"
        ofile.write(message)

canvas.Draw()

#gApplication.Run()

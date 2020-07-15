from pySitrineoAna.config.RunManager import RunManager
from pySitrineoAna.plots.PlotOverlay import PlotOverlay
from pySitrineoAna.plots.TrendPlot import TrendPlot
from pySitrineoAna.code.AnaBeamSpot import *
from ROOT import TFile, gStyle

gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

inputDir="/Users/echabert/Work/taf/Results/"
tafDir="/Users/echabert/Work/taf"
csvfilename="data/CyrceJune2020.csv"
directory = "/Users/echabert/Work/taf/Results/"
odirectory = "Results/AnaBeamSpot/"
#filenamebase = "BeamProfile_run"
filenamebase = "sitrineo"
#runs = [21,35]
runs = [6,8,9,10,14,11,12,13]

print("step 1")
m = RunManager(inputDir,"Results", tafDir)
print("step 2")
m.Load(csvfilename)
print("step 3")
#db = DrawBeamSpots(m,37,[1,5])

#p = PlotOverlay(m,[39,38,41])
#p.SetOptions(False,True)
#print(m.GetListOfHistos(6,"sitrineo"))
#c = p.GetCanvas(filenamebase,"hhitpixpl4")
print("step 5")
#c.Draw()

#p2 = PlotOverlay(m,[59,61,60])
#p2 = PlotOverlay(m,[62,64,63])
#p2 = PlotOverlay(m,[42,44,43])
p2 = PlotOverlay(m,[7,8,9,10,11,12,13])
p2.SetOptions(False,False)
c2 = p2.GetCanvas(filenamebase,"hhitpixpl4")
c2.Print("canv.root")
#

#exit()

"""
#run_8Sig_abs = [39,42,45,48,51,54,59,61]
run_8Sig_abs = [39,42,45,48,51,54,59]
#run_12Sig_abs = [41,44,47,50,53,58]
run_12Sig_abs = [37,41,58]
p3 = PlotOverlay(m,run_12Sig_abs)
p3.SetOptions(False,True,"hnhitspereventpl4")
r = m.GetTAFRootFile(58,"sitrineo")
h=r.Get("hnhitspereventpl4")
print (h.GetMean())
#print("Run 41 - mean #hits: ",m.GetTAFRootFile(41,"sitrineo").Get("hnhitspereventpl4").GetMean())
#print("Run 58 - mean #hits: ",m.GetTAFRootFile(41,"sitrineo").Get("hnhitspereventpl4").GetMean())


c2 = p3.GetCanvas(filenamebase,"hhitpixpl4","thickness")
#c2 = p3.GetCanvas(filenamebase,"hnhitspereventpl4","thickness")
#p4 = PlotOverlay(m,[28,32,34,36,41])
p4 = PlotOverlay(m,[34,35,36])
p4.SetOptions(False,True)
#c2 = p4.GetCanvas(filenamebase,"hhitpixpl4")

db = DrawBeamSpots(m,37,[1,5])
db2 = DrawBeamSpots(m,58,[1,5])
#db = DrawBeamSpots(m,34,[1,100])
#db2 = DrawBeamSpots(m,36,[1,100])
#db3 = DrawBeamSpots(m,70,[1,100])
#db4 = DrawBeamSpots(m,71,[1,100])


import sys
sys.exit(0)

#p = PlotOverlay(m,runs)
#p = PlotOverlay(m,[5,6,7,8])
#print(m.GetListOfHistos(21,"BeamProfile"))
#c = p.GetCanvas("BeamProfile","hhitpixpl4")


#runs = [41,44,47,50,53,56,61,64]
#runs = [42,45,48]#,51,57,62,65]
#runs = [41,42,43,44,45,46,47,50,53,56,61,64]
runs = [41,42,43] #,43,44,45,46,47,50,53,56,61,64]
tplot = TrendPlot(m,runs)
#c = tplot.GetBeamSpot([1,100])
#d = tplot.GetBeamSpot([10,12])
#e = tplot.GetBeamSpot([1,12])

#GetBeamSpots(m, 21)
#db = DrawBeamSpots(m,runs)
db = DrawBeamSpots(m,41,[1,10])

#list the runs: run number, Alu foil thickness [mm]
#runs = [(41,0.2),(44,0.3),(47,0.4),(50,0.5),(53,0.7),(56,0.8),(61,0.9),(64,1.0)]
rlabels = [str(i) for i in runs]
label = "_".join(rlabels)
plotname = "hhitpixpl"
peakSelection = [[2,5,None],[6,9,None],[10,20,None]]
csvfilename = odirectory+"ABS_"+label+".csv"
ofilename = odirectory+"ABSRes_"+label+".root"
ofile = TFile(ofilename,"RECREATE")
csvfile = open(csvfilename,"w")
#for run in runs:
"""
#    results = AnaBeamSpot(inputDir, filenamebase, run, [1,2,3,4], peakSelection, ofile, csvfile) 

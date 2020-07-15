from pySitrineoAna.config import RunManager
from pySitrineoAna.runs import run
from ROOT import TCanvas, TH1F, TH2F, TLegend

class PlotOverlay:
    """
    PlotOverlay class aims to overlay exists graphs produced by TAF
    for several runs
    """
    runs = []
    runManager = None
    filled = False
    normalized = False
    normEntriesPlot = ""
    linewidth = 2
    rootObjects = []

    def __init__(self, runManager,runs):
        """
        runs is the list of run
        Plots could be filled
        Plots could be normalize either to unity or based on the nof entries in a reference plot (1/nof-entries)
        """
        self.runs = runs
        self.runManager = runManager

    def SetOptions(self, filled = False, normalized = False, normEntriesPlot = "", linewidth = 2):
        self.filled = filled
        self.normalized = normalized
        self.linewidth = linewidth
        self.normEntriesPlot = normEntriesPlot

    def SetRuns(self,runs):
        self.runs = runs

    def GetCanvas(self,filebasename,plotname,legLabel = "run"):
        """
           legLabel = legend can be "run", "thickness", "threshold"
        """
        canvas = TCanvas(filebasename+"_".join([str(i) for i in self.runs]))
        leg = TLegend(0.75,0.65,0.85,0.85)
        option="Hist"
        color=2
        for run in self.runs:
            rfile = self.runManager.GetTAFRootFile(run,filebasename)
            if rfile is None: continue
            histo = None
            if isinstance(rfile.Get(plotname),TH1F): 
                histo = TH1F(rfile.Get(plotname))
            if isinstance(rfile.Get(plotname),TH2F): 
                histo = TH2F(rfile.Get(plotname))
                option="COLZ"
            histo.Draw(option)
            histo.SetLineColor(color)
            histo.SetLineWidth(self.linewidth)
            if self.filled: 
                histo.SetFillColor(color)
                #histo.SetFillStyle(4050)
            if self.normalized:
                if self.normEntriesPlot!="" and  (isinstance(rfile.Get(self.normEntriesPlot),TH1F) or isinstance(rfile.Get(self.normEntriesPlot),TH2F)):
                    histoNorm = rfile.Get(self.normEntriesPlot)
                    if  histoNorm.GetEntries()>0:
                        histo.Scale(1./histoNorm.GetEntries())
                else:    
                    if histo.Integral()>0: histo.Scale(1./histo.Integral())
            if legLabel == "run": leg.AddEntry(histo,"Run "+str(run),"l")
            if legLabel == "thickness": leg.AddEntry(histo,"Thickness: "+str(self.runManager.GetRun(run).FoilThickness),"l")
            if legLabel == "threshold": leg.AddEntry(histo,"Thickness: "+str(runManager.GetRun(run).FoilThickness),"l")
            option="hsame"
            color+=1
            leg.Draw("same")
            #import !!!
            #keep in memory
            self.rootObjects.append(rfile)
            self.rootObjects.append(histo)
            self.rootObjects.append(leg)
            ############
        canvas.Update()
        return canvas


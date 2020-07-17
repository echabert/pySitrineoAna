import ROOT
from ROOT import gROOT, TH1F, TCanvas, TF1, TFile, TGraph, TGraphErrors, gApplication, TLegend, TPaveText, TPaveLabel
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
plotMultiName = "hnhitspereventpl"
ofilename = "PixelSize.root"
write = True
logscale = True
scaleToEvents = True
scaleToClusters = False
scaleToBin = False
iBin = 4

ofile = TFile(ofilename,"RECREATE")

#########################################
# Code
#########################################

histosColl = []
canvasColl = []
for channel in range(1,5):
   ofile.cd()
   canvas = TCanvas("Plane "+str(channel))
   canvas.cd()
   leg = TLegend(0.6,0.3,0.85,0.85)
   if logscale:
        canvas.SetLogy()
   color = 1
   first = True
   for run in runs:
      print("Run",run,"channel",channel)
      ifile = TFile(dir+str(run[0])+"/"+filenamebase+str(run[0])+".root")
      ofile.cd()
      plot = TH1F(ifile.Get(plotname+str(channel)))
      plot.GetXaxis().SetRangeUser(0,40)
      plot.GetXaxis().SetTitleOffset(0.8)
      #plot.GetYaxis().SetRangeUser(0,plot.GetMaximum()*3)
      plot.GetYaxis().SetRangeUser(0,3)
      plot.SetLineColor(color)
      histosColl.append(plot)
      color+=1
      if color == 5: color+=1
      plotMulti = TH1F(ifile.Get(plotMultiName+str(channel)))
      leg.AddEntry(plot,"Run "+str(run[0])+" - "+str(plotMulti.GetMean())+" hits/evt","l")
      if scaleToBin:
          plot.Scale(1./plot.GetBinContent(iBin))
      else:
          if scaleToClusters:
            plot.Scale(1./plotMulti.GetMean())
          if scaleToEvents:
            plot.Scale(1./plotMulti.GetEntries())
      if first: 
          plot.Draw("H")
          text = TPaveText(3,plot.GetMaximum()*0.85,15,plot.GetMaximum()*0.98)
          if scaleToBin:
              text.AddText("Normalized to bin "+str(iBin))
          else:
              if scaleToClusters and not scaleToEvents: text.AddText("Normalized to #clusters/evts")
              if not scaleToClusters and scaleToEvents: text.AddText("Normalized to #evts")
              if scaleToClusters and scaleToEvents: text.AddText("Normalized to #clusters")
          text.Draw()
          histosColl.append(text)
          first = False
      else:
        plot.Draw("hsame")
      leg.Draw("same")
      canvas.Update()
      canvas.Modified()
      canvasColl.append(canvas)
      #canvas.WaitPrimitive()
    
   canvas.Update()
   canvas.Modified()
   canvas.WaitPrimitive()
   ofile.cd()
   canvas.Write()

ofile.Write()

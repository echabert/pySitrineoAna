import ROOT
from ROOT import gROOT, TH1F, TCanvas, TF1, TFile, TGraph, gApplication, TLegend
from pySitrineoAna.code.Functions import do3LandauFit
ROOT.gROOT.Reset()
app = ROOT.gApplication
#window = ROOT.gMainWindow(ROOT.gClient.GetRoot(), 200, 200, app)

dir = "/Users/echabert/Work/taf/Results/"
filenamebase = "sitrineo_run"
#list the runs: run number, threholsd [in sigmas]
runs = [(6,5),(8,8),(9,10),(10,12),(14,15),(11,20),(12,25),(13,30)]
plotname = "hhitpixpl"

ofile = TFile("res.root","RECREATE")

canvas = TCanvas()
first = True
color = 2
graphs = []
leg = TLegend(0.6,0.8,0.7,0.9)


f1 = TF1("f1","2*.314*[0]*TMath::Log([1]/(2*3.14*x*[0]))")
#[0]: sigma^2 expressed in pitch^2
#[1]: total charge
for channel in range(1,5):
#for channel in range(1,5):
   print(len(runs))
   ofile.cd()
   graph = TGraph(len(runs)-1)
   graphs.append(graph)
   graph.SetMarkerStyle(21)
   graph.SetMarkerColor(color)
   graph.GetXaxis().SetTitle("Threshold [#sigma]")
   graph.GetYaxis().SetTitle("Mean cluster size")
   leg.AddEntry(graph,"Channel "+str(channel),"P")
   color+=1
   index = 0
   for run in runs:
      ifile = TFile(dir+str(run[0])+"/"+filenamebase+str(run[0])+".root")
      ofile.cd()
      #plot = ifile.Get(plotname+str(channel)).Clone(plotname+str(channel)+"_new")
      plot = TH1F(ifile.Get(plotname+str(channel)))
      plot.GetXaxis().SetRangeUser(3,100)
      #resFit,chi2 = do3LandauFit(plot)
      graph.SetPoint(index,run[1],plot.GetMean())
      #graph.SetPoint(index,run[1],resFit[1]["mpv"])
      print(index,run[1],plot.GetMean())
      index+=1
      #print("Threshold: ",run[1],"mean = ",plot.GetMean(), "mpv = ",plot.GetBinCenter(plot.GetMaximumBin()))
   graph.Fit(f1)
   if first: 
       #plot.Draw()
       ofile.cd()
       canvas.cd()
       graph.Draw("AP")
       first = False
   else: 
       #plot.Draw("same")
       ofile.cd()
       canvas.cd()
       graph.Draw("Psame")
leg.Draw("same")
canvas.Print("canvas.png")

app.Run()

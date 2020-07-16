import ROOT
from ROOT import gROOT, TH1F, TCanvas, TF1, TFile, TGraph, TGraphErrors, gApplication, TLegend
#import sys
#sys.path.append("..")
from pySitrineoAna.base.Functions import do3LandauFit
#import pySitrineoAna.code.Functions  
#from pySitrineoAna.code import Functions 
#from Functions import  do3LandauFit 

ROOT.gROOT.Reset()
app = ROOT.gApplication
#window = ROOT.gMainWindow(ROOT.gClient.GetRoot(), 200, 200, app)


##############################################
# Main program
##############################################

dir = "/Users/echabert/Work/taf/Results/"
#filenamebase = "sitrineo_run"
filenamebase = "BeamProfile_run"
#list the runs: run number, Alu foil thickness [mm]
runs = [(41,0.2),(44,0.3),(47,0.4),(50,0.5),(53,0.7),(56,0.8),(61,0.9),(64,1.0)]
plotname = "hhitpixpl"

ofilename = "Results/AnaWidthThickness.root"
ofile = TFile(ofilename,"RECREATE")

canvasMean = TCanvas("cMean")
canvasNorm = TCanvas("cNorm")
first = True
color = 2
graphs_mpv1 = []
graphs_mpv2 = []
graphs_mpv3 = []
graphs_norm1 = []
graphs_norm2 = []
graphs_norm3 = []
graphs_chi2 = []
leg = TLegend(0.6,0.7,0.85,0.85)


#[0]: sigma^2 expressed in pitch^2
#[1]: total charge
for channel in range(4,5):
#for channel in range(1,5):
#for channel in range(1,5):
   print(len(runs))
   ofile.cd()
   graph_mpv1 = TGraphErrors(len(runs)-1)
   graph_mpv2 = TGraphErrors(len(runs)-1)
   graph_mpv3 = TGraphErrors(len(runs)-1)
   graph_norm1 = TGraphErrors(len(runs)-1)
   graph_norm2 = TGraphErrors(len(runs)-1)
   graph_norm3 = TGraphErrors(len(runs)-1)
   graph_chi2 = TGraphErrors(len(runs)-1)
   graphs_mpv1.append(graph_mpv1)
   graphs_mpv2.append(graph_mpv2)
   graphs_mpv3.append(graph_mpv3)
   graphs_norm1.append(graph_norm1)
   graphs_norm2.append(graph_norm2)
   graphs_norm3.append(graph_norm3)
   graphs_chi2.append(graph_chi2)

   graph_mpv1.SetMarkerStyle(21)
   graph_mpv1.SetMarkerColor(color)
   graph_mpv1.GetXaxis().SetTitle("Alu foil thickness [mm]")
   graph_mpv1.GetYaxis().SetTitle("Mean cluster size")
   graph_mpv2.SetMarkerStyle(21)
   color = 3
   graph_mpv2.SetMarkerColor(color)
   graph_mpv2.GetXaxis().SetTitle("Alu foil thickness [mm]")
   graph_mpv2.GetYaxis().SetTitle("Mean cluster size")
   graph_mpv3.SetMarkerStyle(21)
   color = 4
   graph_mpv3.SetMarkerColor(color)
   graph_mpv3.GetXaxis().SetTitle("Alu foil thickness [mm]")
   graph_mpv3.GetYaxis().SetTitle("Mean cluster size")
   graph_norm1.SetMarkerStyle(21)
   color = 2
   graph_norm1.SetTitle("")
   graph_norm1.SetMarkerColor(color)
   graph_norm1.GetXaxis().SetTitle("Alu foil thickness [mm]")
   graph_norm1.GetYaxis().SetTitle("Normalization")
   graph_norm2.SetMarkerStyle(21)
   color = 3
   graph_norm2.SetMarkerColor(color)
   graph_norm2.GetXaxis().SetTitle("Alu foil thickness [mm]")
   graph_norm2.GetYaxis().SetTitle("Mean cluster size")
   graph_norm3.SetMarkerStyle(21)
   color = 4
   graph_norm3.SetMarkerColor(color)
   graph_norm3.GetXaxis().SetTitle("Alu foil thickness [mm]")
   graph_norm3.GetYaxis().SetTitle("Mean cluster size")
   graph_chi2.SetMarkerStyle(21)
   graph_chi2.SetMarkerColor(color)
   graph_chi2.GetXaxis().SetTitle("Alu foil thickness [mm]")
   graph_chi2.GetYaxis().SetTitle("Mean cluster size")
   

   leg.AddEntry(graph_mpv1,"Cluster Width 3","P")
   leg.AddEntry(graph_mpv2,"Cluster Width 6","P")
   leg.AddEntry(graph_mpv3,"Cluster Width 10 ","P")
   color+=1
   index = 0
   for run in runs:
      ifile = TFile(dir+str(run[0])+"/"+filenamebase+str(run[0])+".root")
      ofile.cd()
      #ifile.ls()
      #plot = ifile.Get(plotname+str(channel)).Clone(plotname+str(channel)+"_new")
      plot = TH1F(ifile.Get(plotname+str(channel)))
      plot.GetXaxis().SetRangeUser(3,100)
      print(plot.GetName()) 
      #Perform the fit
      results, chi2 = do3LandauFit(plot)
      #graph.SetPoint(index,run[1],plot.GetMean())
      #fill the graphs
      graph_mpv1.SetPoint(index,run[1],results[0]["mpv"])
      graph_mpv1.SetPointError(index,0,results[0]["mpvErr"])
      graph_mpv2.SetPoint(index,run[1],results[1]["mpv"])
      graph_mpv2.SetPointError(index,0,results[1]["mpvErr"])
      graph_mpv3.SetPoint(index,run[1],results[2]["mpv"])
      graph_mpv3.SetPointError(index,0,results[2]["mpvErr"])
      graph_norm1.SetPoint(index,run[1],results[0]["norm"])
      graph_norm1.SetPointError(index,0,results[0]["normErr"])
      graph_norm2.SetPoint(index,run[1],results[1]["norm"])
      graph_norm2.SetPointError(index,0,results[1]["normErr"])
      graph_norm3.SetPoint(index,run[1],results[2]["norm"])
      graph_norm3.SetPointError(index,0,results[2]["normErr"])
      graph_chi2.SetPoint(index,run[1],chi2)
      print(index,run[1],plot.GetMean())
      index+=1
      #print("Threshold: ",run[1],"mean = ",plot.GetMean(), "mpv = ",plot.GetBinCenter(plot.GetMaximumBin()))
   if first: 
       #plot.Draw()
       ofile.cd()
       canvasMean.cd()
       graph_mpv1.GetYaxis().SetRangeUser(2,12)
       graph_mpv1.Draw("AP")
       graph_mpv2.Draw("Psame")
       graph_mpv3.Draw("Psame")
       canvasNorm.cd()
       graph_norm1.Draw("AP")
       graph_norm2.Draw("Psame")
       graph_norm3.Draw("Psame")
       first = False
   else: 
       #plot.Draw("same")
       ofile.cd()
       canvas.cd()
       graph.Draw("Psame")
leg.Draw("same")
#canvas.Print("canvas.png")
canvasNorm.Print("Norm_Bump_CWdith_Foils.png")
#app.Run()

#close & save file
canvasMean.Write()
canvasNorm.Write()
ofile.Write()
ofile.Close()
print("################################")
print("# Results saved in: ")
print(" ",ofilename)
print("# Done")
print("################################")



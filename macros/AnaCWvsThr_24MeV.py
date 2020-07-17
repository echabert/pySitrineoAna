import ROOT
from ROOT import gROOT, TH1F, TCanvas, TF1, TFile, TGraph, TGraphErrors, gApplication, TLegend
from pySitrineoAna.base.Functions import do3LandauFit
ROOT.gROOT.Reset()
app = ROOT.gApplication
from pySitrineoAna.dedx.dedxCalculator import dEdxCalculator 
import math


def SearchMaxima(histo, threshold=10):
    """
     Search maxima in an histogram
     Requires that the number of entries is > threshold
     Returns the list of maxima
    """
    maxima = []
    for i in range(1,histo.GetNbinsX()-1):
        x = histo.GetBinContent(i)
        xerr = histo.GetBinError(i)
        xm1 = histo.GetBinContent(i-1)
        xm1err = histo.GetBinError(i-1)
        xp1 = histo.GetBinContent(i+1)
        xp1err = histo.GetBinError(i+1)
        #check that x is the maximum
        #check that the differences are statistically significant
        print(xm1,x,xp1)
        #if x>xp1 and x>xm1 : #and abs(x-xm1)>math.sqrt(xerr*xerr+xm1*xm1) and abs(x-xp1)>math.sqrt(xerr*xerr+xp1err*xp1err):
        #if x>xp1 and x>xm1 and xp1>0 and xm1>0 and x>10: #and abs(x-xm1)>math.sqrt(xerr*xerr+xm1*xm1) and abs(x-xp1)>math.sqrt(xerr*xerr+xp1err*xp1err):
        if x>xp1 and x>xm1 and xp1>0 and x>10: #and abs(x-xm1)>math.sqrt(xerr*xerr+xm1*xm1) and abs(x-xp1)>math.sqrt(xerr*xerr+xp1err*xp1err):
            maxima.append(histo.GetBinCenter(i))
    return maxima

#window = ROOT.gMainWindow(ROOT.gClient.GetRoot(), 200, 200, app)

calc = dEdxCalculator("../config/dEdx.cfg")
dir = "/Users/echabert/Work/taf/Results/"
filenamebase = "sitrineo_run"
#list the runs: run number, threholsd [in sigmas]
runs = [(6,5),(8,8),(9,10),(10,12),(14,15),(11,20),(12,25),(13,30)]
plotname = "hhitpixpl"

ofile = TFile("res.root","RECREATE")
ResFile = open("ResAnavsThr.log","a")

canvas = TCanvas()
canvasTmp = TCanvas()
first = True
color = 2
graphs = []
leg = TLegend(0.6,0.8,0.7,0.9)

fitType = "combi" #gauss or combi
valueType = "mean" #fit , mean or mode
ipeak = 2 # could be peak 1,2 or 3 - only use if valueType = "mode"

dictPeak = {}
with open("peakdictionnary.dat","r") as dictFile:
    for line in dictFile:
        key = line.split()[0]
        run = key.split(",")[0].split("(")[1]
        plane = key.split(",")[1].split(")")[0]
        values = [int(i) for i in line.split()[1:]]
        dictPeak[(int(run),int(plane))] = values
print(dictPeak)

f1 = TF1()
if fitType == "gauss":
    #f1 = TF1("f1","2*3.14*[0]*TMath::Log([1]/(2*3.14*x*[0]))",0,18) # error - pitch^2 is missing
    f1 = TF1("f1","2*TMath::Pi()*[0]/(20.7*20.7)*(TMath::Log([1]/(2*TMath::Pi()*x*[0])))",0,22)
    #[0]: sigma^2 expressed in microns
    #pitch = 20.7 microns
    #[1]: total charge
    #modifier function gaus (sigma, mu) + door (width)
    #define a range to not use last points
    f1.SetParameter(0,400)
    f1.SetParameter(1,200000)
    
else: 
    f1 = TF1("f1","2*TMath::Pi()*[0]/(20.7*20.7)*(TMath::Log([1]/(2*TMath::Pi()*x*[0]))+[2])",0,22)
    f1.SetParameter(0,15)
    f1.SetParameter(1,10)
    f1.SetParameter(2,5)

ResFile.write("###############################\n")
ResFile.write("## Type: "+fitType+" - Peak: "+str(ipeak)+"\n")

for channel in range(1,5):
#for channel in range(1,5):
   print(len(runs))
   ofile.cd()
   graph = TGraphErrors(len(runs)-1)
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
      mean = plot.GetMean()
      canvasTmp.cd()
      if valueType == "mode":
          """
          #search for maximum
          maxima = SearchMaxima(plot,100)
          print("Maximum are: ",maxima)
          #choose one of the peaks
          #if len(maxima)>3: 
          #    imean = maxima
          imean = 1
          if len(maxima)==2:
              if maxima[0]>3 and ipeak>1:
                  imean = int(maxima[ipeak-2])
          if len(maxima)>=3:
              if ipeak == 3:
                  mylist = [i for i in maxima if i>10 and i<25]
                  if len(mylist)>0: imean = int(mylist[0])
                  else: imean = int(maxima[ipeak-1])
              if ipeak == 2:
                  mylist = [i for i in maxima if i>6 and i<18]
                  if len(mylist)>0 and len(mylist)<2: imean = int(mylist[0])
                  if len(mylist)>2: imean = int(mylist[-2])
                  else: imean = int(maxima[ipeak-1])
              if ipeak == 1:
                  mylist = [i for i in maxima if i>0 and i<4]
                  if len(mylist)>0: imean = int(mylist[-1])
                  else: imean = int(maxima[ipeak-1])
            """
          imean = dictPeak[(run[0],channel)][ipeak-1]
          mean = plot.GetBinContent(imean-1)*plot.GetBinCenter(imean-1)\
                  + plot.GetBinContent(imean)*plot.GetBinCenter(imean)\
                  + plot.GetBinContent(imean+1)*plot.GetBinCenter(imean+1)
          mean/=(plot.GetBinContent(imean-1)+plot.GetBinContent(imean)+plot.GetBinContent(imean+1))
          graph.SetPoint(index,run[1],mean)
          graph.SetPointError(index,0,0.5)
          #apply a weighted mean to determine the peak position
      if valueType == "fit":
          #first fit - fit in range mean-std-dev and mean+std-dev
          fLandau = TF1("fLandau","landau",0,30)
          fLandau.SetParameter(1,plot.GetMean())
          fLandau.SetParameter(2,plot.GetStdDev())
          fRes = plot.Fit(fLandau,"S","",plot.GetMean()-plot.GetStdDev(),plot.GetMean()+plot.GetStdDev())
          print(plot.GetMean(),plot.GetStdDev())
          print(fRes.Get().GetParams()[0],fRes.Get().GetParams()[1],fRes.Get().GetParams()[2])
          #second iteration in +/- 2 width
          nwidth = 2.5
          fLandau2 = TF1("fLandau","landau",0,30)
          fLandau2.SetParameter(0,fRes.Get().GetParams()[0])
          fLandau2.SetParameter(1,fRes.Get().GetParams()[1])
          fLandau2.SetParameter(2,fRes.Get().GetParams()[2])
          print("a")
          fRes2 = plot.Fit(fLandau2,"S","",fRes.Get().GetParams()[1]-nwidth*fRes.Get().GetParams()[2],fRes.Get().GetParams()[1]+nwidth*fRes.Get().GetParams()[2])
          print("a")
          print(fRes2.Get().GetParams()[0],fRes2.Get().GetParams()[1],fRes2.Get().GetParams()[2])
          #third iteration
          nwidth = 2
          fLandau2.SetParameter(0,fRes2.Get().GetParams()[0])
          fLandau2.SetParameter(1,fRes2.Get().GetParams()[1])
          fLandau2.SetParameter(2,fRes2.Get().GetParams()[2])
          fRes2 = plot.Fit(fLandau2,"S","",fRes2.Get().GetParams()[1]-nwidth*fRes2.Get().GetParams()[2],fRes2.Get().GetParams()[1]+nwidth*fRes2.Get().GetParams()[2])
          graph.SetPoint(index,run[1],fRes2.Get().GetParams()[1])
          graph.SetPointError(index,0,fRes2.Get().GetCovarianceMatrix()[1][1])
      if valueType == "mean":
          graph.SetPoint(index,run[1],plot.GetMean())
          graph.SetPointError(index,0,plot.GetMeanError())
      #graph.SetPoint(index,run[1],resFit[1]["mpv"])
      print(index,run[1],plot.GetMean())
      index+=1
      #print("Threshold: ",run[1],"mean = ",plot.GetMean(), "mpv = ",plot.GetBinCenter(plot.GetMaximumBin()))
   fitRes = graph.Fit(f1,"RS")
   matrix = fitRes.Get().GetCovarianceMatrix()
   Qtot = 0
   QtotErr = 0
   if fitType == "gauss":
       Qtot = f1.GetParameter(1)
       QtotErr = math.sqrt(matrix[1][1])
   else:
    print(matrix[0][0],matrix[0][1],matrix[0][2])
    print(matrix[1][0],matrix[1][1],matrix[1][2])
    print(matrix[2][0],matrix[2][1],matrix[2][2])
    #evalute the total charge
    Qtot = f1.GetParameter(1)*(f1.GetParameter(2)+1)*188./12
    a = f1.GetParameter(1)
    b = f1.GetParameter(2)
    #QtotErr = math.sqrt(math.pow(1+b,2)*math.pow(matrix[1][1],2)+math.pow(a,2)*math.pow(matrix[2][2],2)+a*b*matrix[1][2])
    #QtotErr = math.sqrt(math.pow(1+b,2)*math.pow(matrix[1][1],2)+math.pow(a,2)*math.pow(matrix[2][2],2))
    QtotErr = math.sqrt(math.pow(1+b,2)*matrix[1][1]+math.pow(a,2)*matrix[2][2])
  
   print("Sigma spatial =",math.sqrt(f1.GetParameter(0))," microns")
   if fitType == "combi":
       print("Width (flat) = ",f1.GetParameter(2),"+/-",math.sqrt(matrix[2][2]))
   print("Charge (tot) = ",Qtot," e-")
   print("Charge error = ",QtotErr," e-")
   print("dEdx = ",calc.GetdEdXFromCharge(Qtot)," MeV.cm2/g")
   #print(calc.GetMomentaFromDeDx(calc.GetdEdXFromCharge(Qtot),2212))
   print("P = ",calc.GetMomentaFromDeDx(calc.GetdEdXFromCharge(Qtot),2212), " MeV")
   
   # Write results in a file
   ResFile.write("## Run "+str(run[0])+" - plane "+str(channel)+"\n")
   ResFile.write("Sigma spatial ="+str(math.sqrt(f1.GetParameter(0)))+" microns\n")
   ResFile.write("Width (flat) = "+str(f1.GetParameter(2))+"+/-"+str(math.sqrt(matrix[2][2]))+"\n")
   ResFile.write("Charge (tot) = "+str(Qtot)+" e-\n")
   ResFile.write("Charge error = "+str(QtotErr)+" e-\n")
   ResFile.write("dEdx = "+str(calc.GetdEdXFromCharge(Qtot))+" MeV.cm2/g\n")
   ResFile.write("dEdx interval = "+str(calc.GetdEdXFromCharge(Qtot-QtotErr))+" - "+str(calc.GetdEdXFromCharge(Qtot+QtotErr))+" MeV.cm2/g\n")
   ResFile.write("P = "+str(calc.GetMomentaFromDeDx(calc.GetdEdXFromCharge(Qtot),2212))+" MeV\n")
   ResFile.write("P interval= "+str(calc.GetMomentaFromDeDx(calc.GetdEdXFromCharge(Qtot-QtotErr),2212))+" - "+str(calc.GetMomentaFromDeDx(calc.GetdEdXFromCharge(Qtot+QtotErr),2212))+" MeV\n")

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
canvas.Print("canvas.root")
ResFile.close()

#app.Run()

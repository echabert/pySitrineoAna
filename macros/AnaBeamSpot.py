import ROOT
from ROOT import gROOT,TEllipse, TH1F, TH2F, TCanvas, TF1, TFile, TGraph, gApplication, TLegend
import copy
import math
from pySitrineoAna.base.BeamSpot import BeamSpot


nxPixels = 960
nyPixels = 928
pitch = 20.4

# inputs:
#   peakSelection [nPixelMin, nPixelMax, TH2F] 
#   planes: [] of plane number
def AnaBeamSpot(ofile, directory, filenamebase, run, planes, peakSelection, logfile = None, nevents=-1):
      # parameters
      nsigma = 1
      
      ifile = TFile(directory+str(run)+"/"+filenamebase+str(run)+".root")
      ofile.cd()
      #print(planes) 
      peakSelections = []
      canvas = []
      for iplane in range(len(planes)):
              #print(iplane)
              #VERY IMPORTANT: NEED TO USE DEEPCOPY TO AVOID TO REUSE THE SAME OBJECT
              newPeakSel = copy.deepcopy(peakSelection)
              # Creation of TH2F
              for ipeak in range(len(peakSelection)):
                  newPeakSel[ipeak][2]=TH2F(str(planes[iplane])+"h2_BS_run_"+str(run)+"_"+str(newPeakSel[ipeak][0])+"-"+str(newPeakSel[ipeak][1])+"_pl"+str(planes[iplane]),"",nxPixels, -nxPixels/2.*pitch,nxPixels/2.*pitch, nyPixels, -nyPixels/2.*pitch, nyPixels/2.*pitch)
              
              peakSelections.append(copy.copy(newPeakSel))

              canvas.append(TCanvas("cBS_run_"+str(run)+"pl"+str(planes[iplane])))
              canvas[iplane].Divide(len(peakSelection))
      #print(peakSelections)
      ####################################
      # Reading the data from TTree
      ####################################
      tree = ifile.Get("mRawTree")
      if nevents==-1 or nevents>tree.GetEntries(): nevents = tree.GetEntries()
      print("Analyze ",nevents,"/",tree.GetEntries(), " events") 
      for ientry in range(nevents):
          if ientry%10000 == 0: print(ientry,"\t/",nevents,end='\r')
          tree.GetEntry(ientry)
          for iplane in range(len(planes)):
             for ipeak in range(len(peakSelections[iplane])):
                if tree.plN == planes[iplane] :
                   if tree.nPixels>=peakSelections[iplane][ipeak][0] and tree.nPixels<=peakSelections[iplane][ipeak][1]: 
                     peakSelections[iplane][ipeak][2].Fill(tree.x,tree.y)
      print("Done !")
      ####################################

      ####################################
      # Drawing
      ####################################
      results = []
      for ipl in range(len(planes)):
         resPlane = []
         for i in range(len(peakSelection)):
            canvas[ipl].cd(i+1)
            peakSelections[ipl][i][2].Draw("COLZ")
            #perform an iterative fit
            # first iteration
            yfit = peakSelections[ipl][i][2].ProjectionY().Fit("gaus","S")
            xfit = peakSelections[ipl][i][2].ProjectionX().Fit("gaus","S")
            # second iteration
            #fit arond the mean and +/- nsigma
            #proection if the pointer is null
            if yfit.Get():
               yfit = peakSelections[ipl][i][2].ProjectionY().Fit("gaus","S","",yfit.Get().GetParams()[1]-nsigma*yfit.Get().GetParams()[2],yfit.Get().GetParams()[1]+nsigma*yfit.Get().GetParams()[2])
            if xfit.Get():
               xfit = peakSelections[ipl][i][2].ProjectionX().Fit("gaus","S","",xfit.Get().GetParams()[1]-nsigma*xfit.Get().GetParams()[2],xfit.Get().GetParams()[1]+nsigma*xfit.Get().GetParams()[2])
            

            #Fill BeamSpot object
            x = 0
            y = 0
            xErr = 0
            yErr = 0
            xwidth = 0
            ywdith = 0
            xwidthErr = 0
            ywidthErr = 0
            if xfit.Get():
                x = xfit.Get().GetParams()[1]
                xErr = xfit.Get().GetErrors()[1]
                xwidth = xfit.Get().GetParams()[2]
                xwidthErr = xfit.Get().GetErrors()[2]
            if yfit.Get():
                y = yfit.Get().GetParams()[1]
                yErr = yfit.Get().GetErrors()[1]
                ywidth = yfit.Get().GetParams()[2]
                ywidthErr = yfit.Get().GetErrors()[2]
            
            bs = BeamSpot(x,xErr,y,yErr,xwidth,xwidthErr,ywidth,ywidthErr)
            #bs = BeamSpot(xfit.Get().GetParams()[1],yfit.Get().GetParams()[1],xfit.Get().GetErrors()[1],yfit.Get().GetErrors()[1],\
            #            xfit.Get().GetParams()[2],yfit.Get().GetParams()[2],xfit.Get().GetErrors()[2],yfit.Get().GetErrors()[2])
            
            #Print results
            print("Run ",run, " Plane ", planes[ipl], "cluster size [",peakSelections[ipl][i][0],"-",peakSelections[ipl][i][1],"] - ", bs.GetStr())
            if logfile is not None: 
                #logfile.write("Run "+str(run)+" Plane "+str(planes[ipl])+"\tcluster size ["+str(peakSelections[ipl][i][0])+"-"+str(peakSelections[ipl][i][1])+"] -\t"+bs.GetStr()+"\n")
                #csv format
                logfile.write(str(run)+","+str(planes[ipl])+","+str(i)+","+bs.GetCSV()+"\n")

            resPlane.append({"bs":bs,"plane":planes[ipl],"wmin":peakSelections[ipl][i][0],"wmax":peakSelections[ipl][i][1]})
         results.append(resPlane)
         canvas[ipl].Write()
      
      ####################################
      # plots of beam spot using ellipses
      ####################################
      cPoints = TCanvas("cBSPoints_"+str(run))
      cPoints.cd()
      BS = TH2F("h2_BSPoints","",nxPixels, -nxPixels/2.*pitch,nxPixels/2.*pitch, nyPixels, -nyPixels/2.*pitch, nyPixels/2.*pitch)
      BS.GetXaxis().SetTitle("X [#mum]")
      BS.GetYaxis().SetTitle("Y [#mum]")
      ires=0
      BS.Draw()
      option="same"
      leg = TLegend(0.65,0.55,0.97,0.97)
      ellipses = []
      indexPeak = 0
      colors = [2,3,4]
      indexPlanes = 0
      fillstyles = [3004,3002,0,0]
      linestyles = [1,2,3,4]
      legOpt = ["f","f","l","l"]
      for result in results:
        indexPeak = 0
        for res in result:
           el = res["bs"].GetEllipseCenter(colors[indexPeak],3,linestyles[indexPlanes],fillstyles[indexPlanes])
           el.Draw(option);
           leg.AddEntry(el,"Plane "+str(res["plane"])+" Width: "+str(res["wmin"])+"-"+str(res["wmax"]),legOpt[indexPlanes])
           ellipses.append(el)
           indexPeak+=1
        indexPlanes+=1
      leg.Draw("same")
      cPoints.Write()
      #print(results)
      
      return results

# Analyse the results from AnaBeamSpot
def BeamSpotSitrineoStudy(results):
    npeaks = 0
    if len(results)>0: npeaks = len(results[0])
    
    print("Analysis of x-shifts")
    for i in range(npeaks):
        print("cluster width [",results[0][i]["wmin"],"-",results[0][i]["wmax"]," ]")
        for j in range(len(results)-1):
            #xshift = results[j+1][i]["bs"].x-results[j][i]["bs"].x
            #print("x-shift [",j+2,",",j+1,"] %0.1f"%xshift, " +/- %0.1f"%math.sqrt(results[j+1][i]["bs"].xErr*results[j+1][i]["bs"].xErr+results[j][i]["bs"].xErr*results[j][i]["bs"].xErr))
            xshift, xshiftErr = results[j][i]["bs"].XShift(results[j+1][i]["bs"])
            print("x-shift [",j+2,",",j+1,"] %0.1f"%xshift, " +/- %0.1f"%xshiftErr)
    
    print("Analysis of multiple scattering")
    for i in range(npeaks):
        print("cluster width [",results[0][i]["wmin"],"-",results[0][i]["wmax"]," ]")
        for j in range(len(results)-1):
            xMS, xMSErr = results[j+1][i]["bs"].xMSWidth(results[j][i]["bs"])
            yMS, yMSErr = results[j+1][i]["bs"].yMSWidth(results[j][i]["bs"])
            print("x-MS [",j+2,",",j+1,"] %0.1f"%xMS, " +/- %0.1f"%xMSErr)
            print("y-MS [",j+2,",",j+1,"] %0.1f"%yMS, " +/- %0.1f"%yMSErr)





#########################################
#   Main program
#########################################


directory = "/Users/echabert/Work/taf/Results/"
odirectory = "Results/AnaBeamSpot/"
#filenamebase = "sitrineo_run"
filenamebase = "BeamProfile_run"
#list the runs: run number, Alu foil thickness [mm]
runs = [(41,0.2),(44,0.3),(47,0.4),(50,0.5),(53,0.7),(56,0.8),(61,0.9),(64,1.0)]
plotname = "hhitpixpl"

#runs at 8 sigma
#runs = [39,42,45,48,51,54,57,62]
#runs = [39,45,48,51,54,57,62]
#runs at 12 sigma
#runs = [41,44,47,50,53,56,61,64]
#runs at 20 sigma
#runs = [40,43,46,49,52,55,60,63]
#final runs
runs = [66,67,68,70,71]
rlabels = [str(i) for i in runs]
label = "_".join(rlabels)


ofilename = odirectory+"ABSRes_"+label+".root"
ofile = TFile(ofilename,"RECREATE")


peakSelection = [[2,5,None],[6,9,None],[10,20,None]]
#peakSelection = [[2,5],[6,9],[10,20]]

csvfilename = odirectory+"ABS_"+label+".csv"
csvfile = open(csvfilename,"w")
for run in runs:
  print("## Run ",run)
  results = AnaBeamSpot(ofile, directory, filenamebase, run, [1,2,3,4], peakSelection, csvfile) 
  BeamSpotSitrineoStudy(results)

ofile.Write()
ofile.Close()
print("################################")
print("# Results saved in: ")
print(" ",ofilename)
print(" ",csvfilename)
print("# Done")
print("################################")
#app.Run()

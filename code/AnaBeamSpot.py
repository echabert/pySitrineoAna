import ROOT
from ROOT import gROOT,TEllipse, TH1F, TH2F, TCanvas, TF1, TFile, TGraph, gApplication, TLegend
import copy
import math
import os
from pySitrineoAna.code.BeamSpot import BeamSpot
from pySitrineoAna.config.RunManager import RunManager

nxPixels = 960
nyPixels = 928
pitch = 20.4

# inputs:
#   peakSelection [nPixelMin, nPixelMax, TH2F] 
#   planes: [] of plane number
def AnaBeamSpot( directory, filenamebase, run, planes, peakSelection, ofile = None, logfile = None, nevents=-1, verbose = False):
      """
      Return a dictionnary of BeamSpot [with info about run, plane and selection
      Return also a TCanvas
      """
      # parameters
      nsigma = 1
      
      if ofile is not None: ofile.cd()

      ifile = TFile(directory+str(run)+"/"+filenamebase+str(run)+".root")
      #print(planes) 
      wmin = 1
      wmax = 100
      if len(peakSelection)>0:
          wmin = peakSelection[0][0]
          wmax = peakSelection[0][1]
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
      outputList = []
      results = []
      bsCollection = []
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
            ywidth = 0
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
            
            #bs = BeamSpot(x,xErr,y,yErr,xwidth,xwidthErr,ywidth,ywidthErr)
            bs = BeamSpot(x,y,xErr,yErr,xwidth,ywidth,xwidthErr,ywidthErr)
            #bs = BeamSpot(xfit.Get().GetParams()[1],yfit.Get().GetParams()[1],xfit.Get().GetErrors()[1],yfit.Get().GetErrors()[1],\
            #            xfit.Get().GetParams()[2],yfit.Get().GetParams()[2],xfit.Get().GetErrors()[2],yfit.Get().GetErrors()[2])
            

            #Print results
            if verbose: print("Run ",run, " Plane ", planes[ipl], "cluster size [",peakSelections[ipl][i][0],"-",peakSelections[ipl][i][1],"] - ", bs.GetStr())
            if logfile is not None: 
                #logfile.write("Run "+str(run)+" Plane "+str(planes[ipl])+"\tcluster size ["+str(peakSelections[ipl][i][0])+"-"+str(peakSelections[ipl][i][1])+"] -\t"+bs.GetStr()+"\n")
                #csv format
                logfile.write(str(run)+","+str(planes[ipl])+","+str(peakSelections[ipl][i][0])+","+str(peakSelections[ipl][i][1])+","+bs.GetCSV()+"\n")

            resPlane.append({"bs":bs,"plane":planes[ipl],"wmin":peakSelections[ipl][i][0],"wmax":peakSelections[ipl][i][1]})
            outputList.append({"bs":bs,"plane":planes[ipl],"wmin":peakSelections[ipl][i][0],"wmax":peakSelections[ipl][i][1]})
            #results.append({"bs":bs,"plane":planes[ipl],"wmin":peakSelections[ipl][i][0],"wmax":peakSelections[ipl][i][1]})
         results.append(resPlane)
         if ofile is not None: 
             ofile.cd()
             canvas[ipl].Write()
      
      ####################################
      # plots of beam spot using ellipses
      ####################################
      cPoints = TCanvas("cBSPoints_"+str(run)+"_"+str(wmin)+"_"+str(wmax))
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
      if ofile is not None: 
          ofile.cd()
          cPoints.Write()
      #print(results)
      
      #return results, cPoints
      return outputList

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



#need to add check of peakselection in if statement
def DrawBeamSpots(runManager, run, peakSelection=[1,100]):
     if runManager.GetRun(run) is not None:
        if "beamspots" in runManager.GetRun(run).__dict__.keys():
            #check if directory exist - otherwise create if
            if os.path.exists(runManager.inputDir+"/"+str(run)):
                filename = runManager.inputDir+"/"+str(run)+"/BeamSpot.root"
                rfile = TFile(filename,"READ")
                canvas = rfile.Get("cBSPoints_"+str(run)+"_"+str(peakSelection[0])+"_"+str(peakSelection[1]))
                if isinstance(canvas,TCanvas):
                    canvas.Draw()
                else:
                    GetBeamSpots(runManager, run, peakSelection)
                    DrawBeamSpots(runManager, run, peakSelection)
                return canvas
        else:
            print("THERE THERE")
            GetBeamSpots(runManager, run, peakSelection)
            DrawBeamSpots(runManager, run, peakSelection)

def GetBeamSpots (runManager, run, peakSelection=[1,100], needToBeRan = False):
    print("WEEEEEEEEEEEEEE")
    if needToBeRan:
            print("ELSE")
            #check if directory exist - otherwise create if
            if not os.path.exists(runManager.inputDir+"/"+str(run)):
                os.mkdir(runManager.inputDir+"/"+str(run))
            #if not found - search if the csv file exists
            csvfilename = runManager.inputDir+"/"+str(run)+"/BeamSpot.csv"
            if os.path.isfile(csvfilename):
                runManager.GetRun(run).beamspots = []
                with open(csvfilename) as ifile:
                    for line in ifile:
                        bs = BeamSpot()
                        print(",".join(line.split(',')[4:]))
                        bs.LoadCSV(",".join(line.split(',')[4:]))
                        element = {}
                        element["bs"] = bs
                        element["plane"] = int(line.split(',')[1])
                        element["wmin"] = int(line.split(',')[2])
                        element["wmax"] = int(line.split(',')[3])
                        runManager.GetRun(run).beamspots.append(element)
                        #runManager.GetRun(run).beamspots = element
        
            else:
                #firstly need to produce the beam sports
                print("Beam spots for run",run,"not found. Need to produce them")
                AddBeamSpots(runManager, run)
            
            return runManager.GetRun(run).beamspots
    
    if runManager.GetRun(run) is not None:
        print("SDDDDDDD")
        print(runManager.GetRun(run).__dict__)
        #needToBeRan = False
        if "beamspots" not in runManager.GetRun(run).__dict__.keys():
            needToBeRan = True
        else:
            print(type(runManager.GetRun(run).beamspots))
            print(type(runManager.GetRun(run).beamspots[0]))
            print(type(peakSelection[0]))
            print(runManager.GetRun(run).beamspots)
            if len([1 for el in runManager.GetRun(run).beamspots if el["wmin"]==peakSelection[0] and el["wmax"]==peakSelection[1]])==0: 
                needToBeRan = True
                GetBeamSpots(runManager,run,peakSelection,needToBeRan)
        if not needToBeRan:
            # new ...
            #check if peakSelection are found
            print("here here")
            beamspots = runManager.GetRun(run).beamspots
            #for sel in peakSelection:
            found=False
            for bs in beamspots:
                print(peakSelection)
                print(bs)
                if peakSelection[0]==bs["wmin"] and peakSelection[1]==bs["wmax"]: found=True
            if not found:
                peakSelection.append(None)
                AddBeamSpots(runManager, run, [peakSelection])
            # end new ..
            return runManager.GetRun(run).beamspots
        #else:
        """
        if needToBeRan:
            print("ELSE")
            #check if directory exist - otherwise create if
            if not os.path.exists(runManager.inputDir+"/"+str(run)):
                os.mkdir(runManager.inputDir+"/"+str(run))
            #if not found - search if the csv file exists
            csvfilename = runManager.inputDir+"/"+str(run)+"/BeamSpot.csv"
            if os.path.isfile(csvfilename):
                runManager.GetRun(run).beamspots = []
                with open(csvfilename) as ifile:
                    for line in ifile:
                        bs = BeamSpot()
                        print(",".join(line.split(',')[4:]))
                        bs.LoadCSV(",".join(line.split(',')[4:]))
                        element = {}
                        element["bs"] = bs
                        element["plane"] = int(line.split(',')[1])
                        element["wmin"] = int(line.split(',')[2])
                        element["wmax"] = int(line.split(',')[3])
                        runManager.GetRun(run).beamspots.append(element)
                        #runManager.GetRun(run).beamspots = element
        
            else:
                #firstly need to produce the beam sports
                print("Beam spots for run",run,"not found. Need to produce them")
                AddBeamSpots(runManager, run)
            
            return runManager.GetRun(run).beamspots
          """
    return None


def AddBeamSpotsMultiRun(runManager, runs):
    for run in runs:
        AddBeamSpots(runManagers, run)

#def AddBeamSpots(runManager, run, planes = [1,2,3,4], peakSelection = [[1,100,None]]):
def AddBeamSpots(runManager, run, peakSelection = [[1,100,None]], planes = [1,2,3,4]):
    """
        Add beam spot for run in runManager using (one/few) selection(s) in cluster size [min, max, None  --> 3rd elementto store histo]
        One can choose the list of planes  [may later depends on a global description
    """
    if runManager.GetRun(run) is not None:
        #add specification for the peak selection ...
        logfile = open(runManager.inputDir+"/"+str(run)+"/BeamSpot.csv","a")
        #change RECREATE to UPDATE
        ofile = TFile(runManager.inputDir+"/"+str(run)+"/BeamSpot.root","UPDATE")
        #runManager.GetRun(run).beamspots = AnaBeamSpot(runManager.inputDir,"BeamProfile_run", run, planes, peakSelection, ofile, logfile )  
        #new
        if "beamspots" in runManager.GetRun(run).__dict__.keys():
            print("HIHI")
            runManager.GetRun(run).beamspots.extend(AnaBeamSpot(runManager.inputDir,"BeamProfile_run", run, planes, peakSelection, ofile, logfile ))  
        else:
            print("We are there !")
            runManager.GetRun(run).beamspots = [AnaBeamSpot(runManager.inputDir,"BeamProfile_run", run, planes, peakSelection, ofile, logfile )]  
        ofile.Write()
        ofile.Close()


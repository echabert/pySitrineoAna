from pySitrineoAna.config import RunManager
from pySitrineoAna.runs import run
from pySitrineoAna.code.AnaBeamSpot import *
from ROOT import TCanvas, TH1F, TH2F, TGraphErrors, TLegend

class TrendPlot:
    """
    PlotPlot class aims to display quantities as function a a-axis variable
    xaxisVar = "runNb", "thickness", "B-field"
   
    Note: later, one could add energy, position ...
    
    """
    runs = []
    runManager = None
    rootObjects = []
    xaxisVar = "runNb"
    rfile = None

    def __init__(self, runManager, runs, xaxisVar="runNb"):
        """
        runs is the list of run
        """
        self.runs = runs
        self.runManager = runManager
        self.xaxisVar = xaxisVar
        self.rfile = TFile("TrendPlot.root","RECREATE")

    #def SetOptions(self, filled = False, normalized = False, linewidth = 2):
    #    self.filled = filled
    #    self.normalized = normalized
    #    self.linewidth = linewidth

    def SetRuns(self,runs):
        self.runs = runs

    def GetBeamSpot(self, peakSelection=[1,100], planes=[1,2,3,4]):
        # position and width (x-y)
        # x-axis variable
        #canvas = TCanvas(filebasename+"_".join([str(i) for i in self.runs]))
        leg = TLegend(0.75,0.65,0.85,0.85)
        #option=""
        #color=2
        #save results in lists
        self.rfile.cd()
        canvas = []
        graphsX = []
        graphsY = []
        graphsXWidth = []
        graphsYWidth = []
        ######################
        npoints = len(self.runs)
        indiceGr=-1
        first = True
        #for run in self.runs:
        print("indice =",indiceGr)

        for plane in planes:
            #print("indice =",indice)
            indiceGr+=1
            print("indice =",indiceGr)
            rindice=-1
            #bspots = GetBeamSpots(self.runManager, run, peakSelection)
            #print(type(bspots))
            #print(bspots)
            wmin = peakSelection[0]
            wmax = peakSelection[1]
            #for bslist in bspots:
            c = TCanvas("c_bs_vs_"+self.xaxisVar+"plane_"+str(plane)+"_sel_"+str(wmin)+"_"+str(wmax))
            c.SetTitle("Plane "+str(plane))
            canvas.append(c)
            graphX = TGraphErrors(npoints)
            graphX.SetName("bsX_trend_"+self.xaxisVar+"plane_"+str(plane)+"_sel_"+str(wmin)+"_"+str(wmax))
            graphX.SetTitle("Beam Spot X")
            graphX.GetXaxis().SetTitle("Run number")
            graphX.GetYaxis().SetTitle("X position [#mum]")
            graphY = TGraphErrors(npoints)
            graphY.SetName("bsY_trend_"+self.xaxisVar+"plane_"+str(plane)+"_sel_"+str(wmin)+"_"+str(wmax))
            graphY.SetTitle("Beam Spot Y")
            graphY.GetXaxis().SetTitle("Run number")
            graphY.GetYaxis().SetTitle("Y position [#mum]")
            graphXWidth = TGraphErrors(npoints)
            graphXWidth.SetName("bsXWidth_trend_"+self.xaxisVar+"plane_"+str(plane)+"_sel_"+str(wmin)+"_"+str(wmax))
            graphXWidth.SetTitle("Beam Spot X Width")
            graphXWidth.GetXaxis().SetTitle("Run number")
            graphXWidth.GetYaxis().SetTitle("X Width [#mum]")
            graphYWidth = TGraphErrors(npoints)
            graphYWidth.SetName("bsYWidth_trend_"+self.xaxisVar+"plane_"+str(plane)+"_sel_"+str(wmin)+"_"+str(wmax))
            graphYWidth.SetTitle("Beam Spot Y Width")
            graphYWidth.GetXaxis().SetTitle("Run number")
            graphYWidth.GetYaxis().SetTitle("Y Width [#mum]")
            graphsX.append(graphX)
            print("plane",plane,"len graphsX",len(graphsX))
            graphsY.append(graphY)
            graphsXWidth.append(graphXWidth)
            graphsYWidth.append(graphYWidth)
            
            #for plane in planes:
            for run in self.runs:
              
              bspots = GetBeamSpots(self.runManager, run, peakSelection)
              rindice+=1 
              for bs in bspots:
               #selection of wmin - wmax
               if bs["wmin"]!=peakSelection[0] or bs["wmax"]!=peakSelection[1]:
                   continue
               #selection of plane
               if bs["plane"] == plane:
                #print(type(bslist))
                #print(bslist)
                #if len(bslist) == 0:
                #    print("pb")

                #rindice+=1
                #bs = bslist[0]
                #bs = bslist
                #indice+=1
                """
                if first :
                    c = TCanvas("c_bs_vs_"+self.xaxisVar+"plane_"+str(bs["plane"])+"_sel_"+str(bs["wmin"])+"_"+str(bs["wmax"]))
                    c.SetTitle("Plane "+str(plane))
                    canvas.append(c)
                    graphX = TGraphErrors(npoints)
                    graphX.SetName("bsX_trend_"+self.xaxisVar+"plane_"+str(bs["plane"])+"_sel_"+str(bs["wmin"])+"_"+str(bs["wmax"]))
                    graphX.SetTitle("Beam Spot X")
                    graphX.GetXaxis().SetTitle("Run number")
                    graphX.GetYaxis().SetTitle("X position [#mum]")
                    graphY = TGraphErrors(npoints)
                    graphY.SetName("bsY_trend_"+self.xaxisVar+"plane_"+str(bs["plane"])+"_sel_"+str(bs["wmin"])+"_"+str(bs["wmax"]))
                    graphY.SetTitle("Beam Spot Y")
                    graphY.GetXaxis().SetTitle("Run number")
                    graphY.GetYaxis().SetTitle("Y position [#mum]")
                    graphXWidth = TGraphErrors(npoints)
                    graphXWidth.SetName("bsXWidth_trend_"+self.xaxisVar+"plane_"+str(bs["plane"])+"_sel_"+str(bs["wmin"])+"_"+str(bs["wmax"]))
                    graphXWidth.SetTitle("Beam Spot X Width")
                    graphXWidth.GetXaxis().SetTitle("Run number")
                    graphXWidth.GetYaxis().SetTitle("X Width [#mum]")
                    graphYWidth = TGraphErrors(npoints)
                    graphYWidth.SetName("bsYWidth_trend_"+self.xaxisVar+"plane_"+str(bs["plane"])+"_sel_"+str(bs["wmin"])+"_"+str(bs["wmax"]))
                    graphYWidth.SetTitle("Beam Spot Y Width")
                    graphYWidth.GetXaxis().SetTitle("Run number")
                    graphYWidth.GetYaxis().SetTitle("Y Width [#mum]")
                    graphsX.append(graphX)
                    graphsY.append(graphY)
                    graphsXWidth.append(graphXWidth)
                    graphsYWidth.append(graphYWidth)
                    first = False
                """
                # x-variable
                #graphsX[0].Draw("ACP")
                xVar = 0
                if self.xaxisVar == "runNb":
                    xVar = run
                    
                print(len(graphsX),indiceGr)
                #print(run,bs["bs"].GetCSV())
                graphsX[indiceGr].SetPoint(rindice,run,bs["bs"].x)
                graphsX[indiceGr].SetPointError(rindice,0.5,bs["bs"].xErr)
                graphsY[indiceGr].SetPoint(rindice,run,bs["bs"].y)
                graphsY[indiceGr].SetPointError(rindice,0.5,bs["bs"].yErr)
                graphsXWidth[indiceGr].SetPoint(rindice,run,bs["bs"].xwidth)
                graphsXWidth[indiceGr].SetPointError(rindice,0.5,bs["bs"].xwidthErr)
                graphsYWidth[indiceGr].SetPoint(rindice,run,bs["bs"].ywidth)
                graphsYWidth[indiceGr].SetPointError(rindice,0.5,bs["bs"].ywidthErr)

                first = False
         
        self.rootObjects.append(self.rfile)
        self.rootObjects.append(canvas)
        for i in range((len(canvas))):
             self.rfile.cd()
             canvas[i].Divide(2,2)
             canvas[i].cd(1)
             #print("mean = ",graphsX[indice].GetMean())
             graphsX[i].Write()
             graphsX[i].Draw("AP")
             canvas[i].cd(2)
             graphsY[i].Draw("AP")
             canvas[i].cd(3)
             graphsXWidth[i].Draw("AP")
             canvas[i].cd(4)
             graphsYWidth[i].Draw("AP")
             canvas[i].Update()
             canvas[i].Write()
        ############
        #canvas.Update()
        return canvas


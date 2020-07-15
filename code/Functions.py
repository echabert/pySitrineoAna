import ROOT
from ROOT import gROOT, TH1F, TCanvas, TF1, TFile, TGraph, TGraphErrors, gApplication, TLegend


# function to fit the cluster size with a sum of 3 landau distribution
# done in range xmin, xmax
# give the initial parameters [norm, mean, width]
def do3LandauFit(histo,xmin=1.5,xmax=15.5,initparams = [[100000,10,0.7],[100000,6,0.5],[30000,3,0.5]]):
    # define the function
    fit = TF1("f1","landau+landau(3)+landau(6)")
    # initialize the parameters
    fit.SetParameter(0,initparams[0][0])
    fit.SetParameter(1,initparams[0][1])
    fit.SetParameter(2,initparams[0][2])
    fit.SetParameter(3,initparams[1][0])
    fit.SetParameter(4,initparams[1][1])
    fit.SetParameter(5,initparams[1][2])
    fit.SetParameter(6,initparams[2][0])
    fit.SetParameter(7,initparams[2][1])
    fit.SetParameter(8,initparams[2][2])
    # perform the fit
    resFit = histo.Fit("f1","S","",xmin,xmax)
    #histo.Fit(f1) #","S","",xmin,xmax)
    #retrive the results of the fit
    norm_3 = fit.GetParameter(0)
    norm_2 = fit.GetParameter(3)
    norm_1 = fit.GetParameter(6)
    normErr_3 = resFit.Get().GetErrors()[0]
    normErr_2 = resFit.Get().GetErrors()[3]
    normErr_1 = resFit.Get().GetErrors()[6]
    mpv_3 = fit.GetParameter(1)
    mpv_2 = fit.GetParameter(4)
    mpv_1 = fit.GetParameter(7)
    mpvErr_3 = resFit.Get().GetErrors()[1]
    mpvErr_2 = resFit.Get().GetErrors()[4]
    mpvErr_1 = resFit.Get().GetErrors()[7]
    chi2 = resFit.Get().Chi2()/resFit.Get().Ndf()
    #print(mpv_2,mpv_3)
    results = [{"mpv":mpv_1,"mpvErr":mpvErr_1,"norm":norm_1,"normErr":normErr_1},\
               {"mpv":mpv_2,"mpvErr":mpvErr_2,"norm":norm_2,"normErr":normErr_2},\
               {"mpv":mpv_3,"mpvErr":mpvErr_3,"norm":norm_3,"normErr":normErr_3}]
    return results, chi2


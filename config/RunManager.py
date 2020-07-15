#import pySitrineoAna.runs 
from pySitrineoAna.runs import run
import os
import subprocess
import shlex
from ROOT import TFile

############################
# Class to manage runs
############################


# check if rootfile exists
# can be ran
# 

class RunManager:

    def __init__(self):
        self.runs = []
        self.tafDir = ""
        self.inputDir = ""
        self.outputDir = ""
        self.templateFilename = "MacroTAF.C.tpl"

    def __init__(self, inputDir, outputDir, tafDir, template="MacroTAF.C.tpl"):
        """
            List or runs
            Directory where TAF is installed
            Directory where TAF output are store
            Directory where outputs will be store
        """
        self.runs = []
        self.tafDir = tafDir
        self.inputDir = inputDir
        self.outputDir = outputDir
        self.templateFilename = template

    def Load(self,configfile):
        """ Load a list from a formatted csv file """
        with open(configfile,encoding="utf8", errors='ignore') as f:
            for line in f:
                #print(line)
                self.runs.append(run.Run(line))

    
    def ExportCSV(self,ofilename,mode='w'):
        """Export runs in a file  with csv format
        Could be in mode 'w', 'a'
        """
        with open(ofilename,mode) as ofile:
            for run in self.runs:
                ofile.write(run.GetCSVFormat())

    def GetRun(self,number):
        for run in self.runs:
            if run.nb == number:
                return run
        return None


    def AddRun(self,run):
        """ add a variable of type Run """
        #check type
        if isinstance(run,Run):
            self.runs.append(run)
            return True
        else:
            return False

    def TAFResAvailable(self,number, filebasename=""):
        """ Check if TAF output are available """
        #if not os.path.isdir(self.outputdir+"/"+str(number)):
        #    print("TAF not ran for run", number)
        #    return False
        print("search for ",self.inputDir+"/"+str(number)+"/"+filebasename+"_run"+str(number)+".root")
        if filebasename !="" and os.path.isfile(self.inputDir+"/"+str(number)+"/"+filebasename+"_run"+str(number)+".root"):
            return True
        else:
            return False


    def GetListOfHistos(self, runnumber, filebasename):
        rfile = self.GetTAFRootFile(runnumber,filebasename)
        #rfile.ls()
        histoList = [i.GetName() for i in rfile.GetListOfKeys() if i.GetClassName()=="TH1F" or i.GetClassName()=="TH2F"]
        return histoList

    def RunTAF(self,number):
        macroFilename = "MacroTAF.C"
        #print([i.nb for i in self.runs])
        if number not in [i.nb for i in self.runs]:
            print("Run", number,"not in the list of runs")
            return False
        NofEvts = [i.nevts for i in self.runs][0]
        template = open(self.tafDir+"/"+self.templateFilename)
        filecontent = template.read().replace("RUN",str(number))
        filecontent = filecontent.replace("NOFEVENTS",str(NofEvts))
        macroFile = open(self.tafDir+"/"+macroFilename)
        print(filecontent)
        #built the command - need to move to TAF directory
        command ="env -i bash -c 'source ~/.bashrc && "
        #command += "source /Users/echabert/Work/root6.19/build/bin/thisroot.sh &&"
        command += "source /Users/echabert/Work/root6.18/bin/thisroot.sh &&"
        command += "cd "+self.tafDir+" &&"
        command += "source Scripts/thistaf.sh &&"
        command += "taf -cfg config/Run"+str(number)+".cfg "+macroFilename +" &&"
        command += "cd - '"
        print(command)
        #Launch the command
        print("Running TAF for run",number)
        #process = subprocess.run(command, shell=True, check=True)
        pwd = os.getcwd()
        os.chdir(self.tafDir)
        #process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        #process = subprocess.run(command, shell=True, check=True)
        #os.system(command)
        #subprocess.call(command.split())
        command = shlex.split(command)
        proc = subprocess.Popen(command, stdout = subprocess.PIPE)
        os.chdir(pwd)
        return True

    def GetTAFRootFile(self,number, filebasename=""):
        """Access ROOT File produced from ROOT"""
        if self.TAFResAvailable(number, filebasename):
            return (TFile(self.inputDir+"/"+str(number)+"/"+filebasename+"_run"+str(number)+".root","READ"))
        else:
            print("Need to run TAF  for run",number)
            self.RunTAF(number)
            return None

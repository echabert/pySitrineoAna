
############################
# Class describing a run
############################

class Run:

    def __init__(self):
        self.nb = -1
        self.nevts = -1

        ###################
        # setup related
        ###################
        
        # type could be 'beam', 'noise', 'source' 
        self.type = ''
        self.collimator = False
        self.magnet = False
        self.BField = 0
        #if degrador
        self.FoilThickness = 0

        # DAQ
        self.DaqVersion = 'daqSoc_3'
        self.threshold = -1

        # Comments
        self.comments = ''


    def __init__(self,csvline):
        """ load data from formatted cvs file line """
        csvlist = csvline.split(",")
        if len(csvlist) < 10:
            self = Run 
            print("incorrect format")
        else:
            self.nb = int(csvlist[0])
            self.nevts = int(csvlist[1])
            self.type = csvlist[2]
            self.collimator = bool(int(csvlist[3]))
            self.magnet = bool(int(csvlist[4]))
            self.BField = float(csvlist[5])
            self.FoilThickness = float(csvlist[6])
            self.DaqVersion = csvlist[7]
            self.threshold = int(csvlist[8])
            self.comments = csvlist[9]

    def GetCSVFormat(self):
        output = str(self.nb)+","
        output+= str(self.nevts)+","
        output+= self.type+","
        output+= str(self.collimator)+","
        output+= str(self.magnet)+","
        output+= str(self.BField)+","
        output+= str(self.FoilThickness)+","
        output+= str(self.DaqVersion)+","
        output+= str(self.threshold)+","
        output+= self.comments+"\n"
        return output

    def __str__(self):
        output = "Run "+str(self.nb)+" - "+str(self.nevts)+" evts - type: "+self.type+" thr="+str(self.threhsold)
        return output
     

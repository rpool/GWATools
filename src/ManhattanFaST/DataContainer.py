import re
import gzip
import scipy
import pylab
import copy
import colorsys

import Logger

class DataContainer:
    def __init__(self):
        self.DataName  = None
        self.DataArray = None
        return

    def SetDataName(self,
                    Name=str):
        self.DataName = Name
        return

    def GetDataName(self):
        return self.DataName

    def InitDataArray(self):
        self.DataArray = []
        return

    def AppendToArray(self,
                      Entry=str):
        self.DataArray.append(Entry)
        return

    def GetDataArray(self):
        return self.DataArray


class DataContainers:
    def __init__(self):
        self.Name2Column       = {}
        self.Column2Name       = {}
        self.DataContainers    = {}
        self.SnpPositionDict   = None
        self.SnpChrDict        = None
        self.XMinMaxPerChrDict = None
        self.iLARGE            = 1e200
        self.Label             = ''
        self.Color             = None
        return

    def ParseFaSTGWAOutput(self,
                           FileName=str,
                           Log=Logger):
        LogString = '**** Parsing fastlmm output file \"'+FileName+'\" ...'
        print LogString
        Log.Write(LogString+'\n')

        for Entry in FileName.split('_'):
            if(re.search('Chunk',Entry)):
                self.Label = Entry

        fr = None
        if(re.search('.gz',FileName)):
            fr = gzip.open(FileName,'r')
        else:
            fr = open(FileName,'r')

        Header      = fr.readline()
        CountColumn = 0
        for Name in Header.strip().split():
            self.DataContainers[Name]     = DataContainer()
            self.Column2Name[CountColumn] = Name
            self.Name2Column[Name]        = CountColumn
            self.DataContainers[Name].SetDataName(Name)
            self.DataContainers[Name].InitDataArray()
            CountColumn                  += 1
        for Line in fr:
            LSplit = Line.strip().split()
            for i in range(len(LSplit)):
                Entry = LSplit[i]
                Name  = self.Column2Name[i]
                self.DataContainers[Name].AppendToArray(Entry)

        if(type(fr)==file):
            fr.close()

        return

    def ParseSnpInfoFile(self,
                         FileName=str,
                         Log=Logger):
        LogString = '**** Parsing SNP info file \"'+FileName+'\" ...'
        print LogString
        Log.Write(LogString+'\n')

        fr                   = open(FileName,'r')
        Header               = fr.readline().strip().split(',')
        Counter              = 0
        SnpPositionColumn    = None
        SnpRsIdColumn        = None
        SnpChrColumn         = None
        self.SnpPositionDict = {}
        self.SnpChrDict      = {}
        for Entry in Header:
            if(Entry=='rsid'):
                SnpRsIdColumn = Counter
            if(Entry=='CHR'):
                SnpChrColumn = Counter
            if(Entry=='pos'):
                SnpPositionColumn = Counter
            Counter += 1

        for Line in fr:
            LSplit = Line.strip().split(',')

            RsId   = LSplit[SnpRsIdColumn]
            Pos    = LSplit[SnpPositionColumn]
            Chr    = LSplit[SnpChrColumn]

            self.SnpPositionDict[RsId] = Pos
            self.SnpChrDict[RsId]      = Chr
        fr.close()

        self.XMinMaxPerChrDict = {}
        for Key,Value in self.SnpChrDict.iteritems():
            if(not self.XMinMaxPerChrDict.has_key(Value)):
                self.XMinMaxPerChrDict[Value] = [self.iLARGE,
                                                 -self.iLARGE]
            self.XMinMaxPerChrDict[Value] = [min(self.XMinMaxPerChrDict[Value][0],
                                                 int(self.SnpPositionDict[Key])),
                                             max(self.XMinMaxPerChrDict[Value][1],
                                                 int(self.SnpPositionDict[Key]))]

        return


    def PylabUpdateParams(self):
        figwidth_pt   = 948.0 # pt (from revtex \showthe\columnwidth)
#        figwidth_pt   = 246.0 # pt (from revtex \showthe\columnwidth)
        inches_per_pt = 1.0/72.27
        figwidth      = figwidth_pt*inches_per_pt
        golden_mean   = (scipy.sqrt(5.0)-1.0)/2.0 # Aesthetic ratio
        figheight     = figwidth*golden_mean
        fig_size      = [figwidth,figheight]
        params        = {'backend': 'pdf',
                         'patch.antialiased': True,
                         'axes.labelsize': 10,
                         'axes.linewidth': 0.5,
                         'grid.color': '0.75',
                         'grid.linewidth': 0.25,
                         'grid.linestyle': ':',
                         'axes.axisbelow': False,
                         'text.fontsize': 10,
                         'legend.fontsize': 5,
                         'xtick.labelsize': 10,
                         'ytick.labelsize': 10,
                         'text.usetex': True,
                         'figure.figsize': fig_size}
        left   = 0.16
        bottom = 0.16
        width  = 0.86-left
        height = 0.95-bottom

        return params,\
               [left, bottom, width, height]

    def PlotManhattan(self,
                      xname=str,
                      yname=str,
                      Log=Logger):

        LogString = '**** Generating Manhattan plot ...'
        print LogString
        Log.Write(LogString+'\n')

        XName = ''
        YName = ''
        for Key in self.DataContainers.iterkeys():
            if(re.search(xname,Key)):
                XName = Key
            if(re.search(yname,Key)):
                YName = Key

        X = []
        for Entry in self.DataContainers[XName].GetDataArray():
            X.append(int(Entry))
        X = scipy.array(X)
        Y = []
        for Entry in self.DataContainers[YName].GetDataArray():
            if(Entry=='-1'):
                Y.append(float(1.0))
            else:
                Y.append(float(Entry))
        Y = -scipy.log10(scipy.array(Y))

        PylabParameters,\
        Rectangle         = self.PylabUpdateParams()
        pylab.rcParams.update(PylabParameters)
        PylabFigure = pylab.figure()
        PylabFigure.clf()
        PylabAxis = PylabFigure.add_axes(Rectangle)
        PylabAxis.scatter(x=X,
                          y=Y)
        XSign = scipy.array(PylabAxis.get_xlim())
        YSign = -scipy.log10(scipy.array([5.0e-8,5.0e-8]))
        PylabAxis.plot(XSign,
                       YSign,
                       linestyle='--',
                       color='grey',
                       linewidth=1.0)
        XSugg = scipy.array(PylabAxis.get_xlim())
        YSugg = -scipy.log10(scipy.array([1.0e-5,1.0e-5]))
        PylabAxis.plot(XSugg,
                       YSugg,
                       linestyle=':',
                       color='grey',
                       linewidth=1.0)
        PylabAxis.set_ylim([0.0,PylabAxis.get_ylim()[1]])
        PylabFigure.savefig('Manhattan.png')
        PylabAxis.clear()
        pylab.close(PylabFigure)
        del PylabFigure
        del PylabAxis

        return

class ListDataContainers:
    def __init__(self):
        self.List              = []
        self.PhenotypeName     = ''
        self.SnpPositionDict   = None
        self.SnpChrDict        = None
        self.OffsetPerChr      = None
        self.XMinMaxPerChrDict = None
        self.RGBTupleDict      = None
        self.OffsetBetweenChrs = 0
        return

    def SetColorsPerChr(self,
                        boGreyScale=bool,
                        NChr=int):
        HSV_tuples = None
        RGB_tuples = None
        if(boGreyScale):
            boGrey     = True
            GreyHSV    = (0.0,0.0,0.4)
            BlackHSV   = (0.0,0.0,0.0)
            HSV_tuples = []
            for i in range(NChr):
                if(boGrey):
                    HSV_tuples.append(GreyHSV)
                    boGrey = False
                else:
                    HSV_tuples.append(BlackHSV)
                    boGrey = True
            RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
        else:
            HSV_tuples = [(x*1.0/NChr, 0.75, 0.75) for x in range(NChr)]
            RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)

        self.RGBTupleDict = {}
        for i in range(len(RGB_tuples)):
            Tuple = RGB_tuples[i]
            Chr   = str(i+1)
            self.RGBTupleDict[Chr] = Tuple
        return

    def SetOffsetPerChr(self):
        self.OffsetPerChr = {}
        for Key in self.XMinMaxPerChrDict.iterkeys():
            if(Key=='1'):
                self.OffsetPerChr[Key] = 0
            else:
                self.OffsetPerChr[Key]  = self.XMinMaxPerChrDict[str(int(Key)-1)][1]
        Keys = []
        for Key in self.OffsetPerChr.iterkeys():
            Keys.append(int(Key))
        Keys.sort()
        SumOffset = self.OffsetPerChr[str(Keys[0])]
        for i in range(1,len(Keys)):
            Key                     = str(Keys[i])
            SumOffset              += self.OffsetPerChr[Key]
            self.OffsetPerChr[Key]  = SumOffset
        return

    def SetPhenotypeName(self,
                         Name=str):
        self.PhenotypeName = Name
        return

    def GetPhenotypeName(self):
        return self.PhenotypeName


    def PylabUpdateParams(self):
        figwidth_pt   = 1422.0 # pt (from revtex \showthe\columnwidth)
#        figwidth_pt   = 246.0 # pt (from revtex \showthe\columnwidth)
        inches_per_pt = 1.0/72.27
        figwidth      = figwidth_pt*inches_per_pt
        golden_mean   = (scipy.sqrt(5.0)-1.0)/2.0 # Aesthetic ratio
        figheight     = figwidth*golden_mean
        fig_size      = [figwidth,figheight]
        params        = {'backend': 'pdf',
                         'patch.antialiased': True,
                         'axes.labelsize': 18,
                         'axes.linewidth': 0.5,
                         'grid.color': '0.75',
                         'grid.linewidth': 0.25,
                         'grid.linestyle': ':',
                         'axes.axisbelow': False,
                         'text.fontsize': 14,
                         'legend.fontsize': 14,
                         'xtick.labelsize': 14,
                         'ytick.labelsize': 14,
                         'text.usetex': True,
                         'figure.figsize': fig_size}
        left   = 0.06
        bottom = 0.10
        width  = 0.95-left
        height = 0.95-bottom

        return params,\
               [left, bottom, width, height]

    def PlotManhattan(self,
                      xname=str,
                      yname=str,
                      Log=Logger):

        LogString = '**** Generating Manhattan plot ...'
        print LogString
        Log.Write(LogString+'\n')

        PylabParameters,\
        Rectangle         = self.PylabUpdateParams()
        pylab.rcParams.update(PylabParameters)
        PylabFigure = pylab.figure()
        PylabFigure.clf()
        PylabAxis   = PylabFigure.add_axes(Rectangle)
        XMax        = 0
        XTicks      = []
        XTickLabels = []
        Keys        = []
        for Key in self.XMinMaxPerChrDict.iterkeys():
            Keys.append(int(Key))
        Keys.sort()
        for Key in Keys:
            XMinMax = self.XMinMaxPerChrDict[str(Key)]
            XTicks.append(0.5*(XMinMax[0]+XMinMax[1])+self.OffsetPerChr[str(Key)]+self.OffsetBetweenChrs)
            XTickLabels.append(r'${\rm CHR'+str(Key)+'}$')
        XMax = self.XMinMaxPerChrDict[str(Keys[-1])][1]+\
               self.OffsetPerChr[str(Keys[-1])]+\
               self.OffsetBetweenChrs*(len(Keys)-1)
        del Keys
        for i in range(len(self.List)):
            DCs   = self.List[i]
            XName = ''
            YName = ''
            for Key in DCs.DataContainers.iterkeys():
                if(xname==Key):
                    XName = Key
                if(yname==Key):
                    YName = Key

            X      = []
            Y      = []
            Colors = []
            for j in range(len(DCs.DataContainers[YName].GetDataArray())):
                YEntry = DCs.DataContainers[YName].GetDataArray()[j]
                xx     = None
                if(xname=='SNP'):
                    RsId    = DCs.DataContainers[XName].GetDataArray()[j]
                    Chr     = self.SnpChrDict[RsId]
                    Offset  = self.OffsetPerChr[Chr]
                    xx      = self.SnpPositionDict[RsId]
                    xx      = str(int(xx) + Offset + self.OffsetBetweenChrs)
                    Colors.append(list(self.RGBTupleDict[Chr]))
                else:
                    xx = DCs.DataContainers[XName].GetDataArray()[j]
                    Colors.append(list(self.RGBTupleDict[str(i+1)]))
                XEntry = xx
                if(YEntry!='NA'):
                    Y.append(float(YEntry))
                    X.append(int(XEntry))
                else:
                    Y.append(1.0)
                    X.append(int(XEntry))
            if(not xname=='SNP'):
                XTicks.append(0.5*(min(X)+max(X))+XMax)
                XTickLabels.append(r'${\rm '+DCs.Label+'}$')
                X    = scipy.array(X) + XMax
                XMax = X.max()+self.OffsetBetweenChrs
            Y = -scipy.log10(scipy.array(Y))

            YInsign = Y < -scipy.log10(1.0e-6)
            YSign   = Y > -scipy.log10(5.0e-8)
            YSugg   = Y >= -scipy.log10(1.0e-6)
            YSugg  *= Y <= -scipy.log10(5.0e-8)

            LogString = '**** Processing Chunk '+str(i+1)+' ...'
            print LogString
            Log.Write(LogString+'\n')

            YY = scipy.compress(YInsign,Y)
            if(len(YY)>0):
                ColorsCopy = []
                for i in range(len(Colors)):
                    if(YInsign[i]):
                        ColorsCopy.append(Colors[i])
                PylabAxis.scatter(x=scipy.compress(YInsign,X),
                                  y=YY,
                                  color=ColorsCopy,
                                  s=0.5)
                del ColorsCopy
            YY = scipy.compress(YSugg,Y)
            if(len(YY)>0):
                ColorsCopy = []
                for i in range(len(Colors)):
                    if(YSugg[i]):
                        ColorsCopy.append(Colors[i])
                PylabAxis.scatter(x=scipy.compress(YSugg,X),
                                  y=YY,
                                  color=ColorsCopy,
                                  s=5.0)
                del ColorsCopy
            YY = scipy.compress(YSign,Y)
            if(len(YY)>0):
                ColorsCopy = []
                for i in range(len(Colors)):
                    if(YSign[i]):
                        ColorsCopy.append(Colors[i])
                PylabAxis.scatter(x=scipy.compress(YSign,X),
                                  y=YY,
                                  color=ColorsCopy,
                                  s=10.0)
                del ColorsCopy

        XSign = scipy.array(PylabAxis.get_xlim())
        YSign = -scipy.log10(scipy.array([5.0e-8,5.0e-8]))
        PylabAxis.plot(XSign,
                       YSign,
                       linestyle='--',
                       color='grey',
                       label=r'${\rm '+self.PhenotypeName+'}$',
                       linewidth=1.25)
        XSugg = scipy.array(PylabAxis.get_xlim())
        YSugg = -scipy.log10(scipy.array([1.0e-6,1.0e-6]))
        PylabAxis.plot(XSugg,
                       YSugg,
                       linestyle=':',
                       color='grey',
                       linewidth=1.25)
        PylabAxis.set_ylim([0.0,PylabAxis.get_ylim()[1]])
#        PylabAxis.set_xlim([-5e7,PylabAxis.get_xlim()[1]])
        PylabAxis.set_xlim([0,XMax])
        Handles,Labels = PylabAxis.get_legend_handles_labels()
        PylabAxis.legend(Handles,
                         Labels,
                         fancybox=True,
                         shadow=True,
                         loc='best')
        PylabAxis.set_xlabel(r'$\rm position$')
        PylabAxis.spines['right'].set_visible(False)
        PylabAxis.spines['top'].set_visible(False)
        PylabAxis.xaxis.set_ticks_position('bottom')
        PylabAxis.yaxis.set_ticks_position('left')
        PylabAxis.xaxis.set_ticks(XTicks)
        PylabAxis.xaxis.set_ticklabels(XTickLabels)
        for Label in PylabAxis.xaxis.get_ticklabels():
            Label.set_rotation(90)
        PylabAxis.set_ylabel(r'$-{\rm log}_{10}(p-{\rm value})$')
        PylabFigure.savefig('Manhattan_'+self.PhenotypeName+'.png')
        PylabAxis.clear()
        pylab.close(PylabFigure)
        del PylabFigure
        del PylabAxis

        return
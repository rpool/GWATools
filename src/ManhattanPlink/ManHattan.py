#! /usr/bin/env python
import os
import re
import colorsys
import copy

import ArgumentParser
import Logger
import DataContainer

def main(ExecutableName):

    ArgParser,\
    Arguments   = ArgumentParser.ParseArguments()

    Ext = ''
    Log = Logger.Logger(ExecutableName,
                        Ext)
    LogString  = '## START TIMESTAMP\n'
    LogString += str(Log.GetStartDate())+'\n'
    LogString += '## END TIMESTAMP'
    print LogString
    Log.Write(LogString+'\n')
    LogString = Log.GetStartLogString()
    print LogString
    Log.Write(LogString+'\n')
    ArgumentParser.LogArguments(Log,
                                ArgParser,
                                Arguments)

    if(Arguments.PlinkOutputFile!=None):
        DCs = DataContainer.DataContainers()
        DCs.ParsePlinkGWAOutput(Arguments.PlinkOutputFile,
                                Log)
        DCs.ParseSnpInfoFile(Arguments.SnpInfoFile,
                             Log)
        DCs.PlotManhattan(xname='pos',
                          yname='pvalue',
                          Log=Log)
    else:
        PlinkOutputFiles = []
        for File in os.listdir(Arguments.PlinkOutputPath):
            if((re.search(Arguments.PlinkOutputPreExtStr,File)) and
               (not re.search('.log',File))):
                PlinkOutputFiles.append(File)
#        for p in range(Arguments.NPhe):
        for p in range(78,79):
            P     = '_PHE'+str(p+1)+'_'
            Files = []
#            for c in range(2):
            for c in range(Arguments.NChr):
                C = '_CHR'+str(c+1)+'_'
                for File in PlinkOutputFiles:
                    if(re.search(P,File) and
                       re.search(C,File)):
                        Files.append(File)
            DCsList = DataContainer.ListDataContainers()
            DCsList.SetPhenotypeName(re.sub('_','',P))

            HSV_tuples = None
            RGB_tuples = None
            if(Arguments.boGreyScale):
                boGrey     = True
                GreyHSV    = (0.0,0.0,0.4)
                BlackHSV   = (0.0,0.0,0.0)
                HSV_tuples = []
                for i in range(len(Files)):
                    if(boGrey):
                        HSV_tuples.append(GreyHSV)
                        boGrey = False
                    else:
                        HSV_tuples.append(BlackHSV)
                        boGrey = True
                RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
            else:
                HSV_tuples = [(x*1.0/len(Files), 0.75, 0.75) for x in range(len(Files))]
                RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
            boParsedSnpInfo = False
            for i in range(len(Files)):
                File = Files[i]
                DCs  = DataContainer.DataContainers()

                DCs.Color = RGB_tuples[i]
                DCs.ParsePlinkGWAOutput(os.path.join(Arguments.PlinkOutputPath,File),
                                        Log)
                if(not boParsedSnpInfo):
                    DCs.ParseSnpInfoFile(Arguments.SnpInfoFile,
                                         Log)
                    boParsedSnpInfo = True
                DCsList.List.append(DCs)
            DCsList.SnpChrDict                = copy.deepcopy(DCsList.List[0].SnpChrDict)
            DCsList.SnpPositionDict           = copy.deepcopy(DCsList.List[0].SnpPositionDict)
            DCsList.XMinMaxPerChrDict         = copy.deepcopy(DCsList.List[0].XMinMaxPerChrDict)
            DCsList.List[0].SnpChrDict        = None
            DCsList.List[0].SnpPositionDict   = None
            DCsList.List[0].XMinMaxPerChrDict = None

            DCsList.PlotManhattan(xname='SNP',
                                  yname='P',
                                  Log=Log)

    LogString = '**** Done :-)'
    print LogString
    Log.Write(LogString+'\n')
    LogString = Log.GetEndLogString()
    print LogString
    Log.Write(LogString+'\n')
    Log.Close()

    return

if(__name__=='__main__'):
    ExecutableName = os.path.abspath(__file__).split('/')[-1]
    main(ExecutableName)
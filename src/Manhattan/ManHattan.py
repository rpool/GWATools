#! /usr/bin/env python
import os
import re
import colorsys

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
    if(Arguments.SnpTestOutputFile!=None):
        DCs = DataContainer.DataContainers()
        DCs.ParseSnpTestGWAOutput(Arguments.SnpTestOutputFile,
                                  Log)
        DCs.PlotManhattan(xname='pos',
                          yname='pvalue',
                          Log=Log)
    else:
        SnpTestOutputFiles = []
        for File in os.listdir(Arguments.SnpTestOutputPath):
            if((re.search(Arguments.SnpOutputPreExtStr,File)) and
               (not re.search('.log',File))):
                SnpTestOutputFiles.append(File)
        for p in range(Arguments.NPhe):
#        for p in range(157,Arguments.NPhe):
            P     = '_PHE'+str(p+1)+'_'
            Files = []
#            for c in range(1):
            for c in range(Arguments.NChr):
                C = '_CHR'+str(c+1)+'_'
                for File in SnpTestOutputFiles:
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
            for i in range(len(Files)):
                File = Files[i]
                DCs  = DataContainer.DataContainers()
                DCs.ParseSnpTestGWAOutput(os.path.join(Arguments.SnpTestOutputPath,File),
                                          Log)
                DCs.Color = RGB_tuples[i]
                DCsList.List.append(DCs)
            DCsList.PlotManhattan(xname='pos',
                                  yname='pvalue',
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
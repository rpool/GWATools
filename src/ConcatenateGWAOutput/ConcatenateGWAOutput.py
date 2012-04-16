#! /usr/bin/env python
import os
import re
import gzip

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

    SnpTestOutputFiles = []
    for File in os.listdir(Arguments.SnpTestOutputPath):
        if((re.search(Arguments.SnpOutputPreExtStr,File)) and
           (not re.search('.log',File)) and
           (not re.search('.swp',File))):
            SnpTestOutputFiles.append(File)
    for p in range(Arguments.NPhe):
#    for p in range(111,112):
#        for p in range(157,Arguments.NPhe):
        P       = '_PHE'+str(p+1)+'_'
        DCsList = DataContainer.ListDataContainers()
        DCsList.SetPhenotypeName(re.sub('_','',P))

        Files = []
#        for c in range(19,21):
        for c in range(Arguments.NChr):
            C = '_CHR'+str(c+1)+'_'
            for File in SnpTestOutputFiles:
                if(re.search(P,File) and
                   re.search(C,File)):
                    Files.append(File)
        for i in range(len(Files)):
            File = Files[i]
            DCs  = DataContainer.DataContainers()
            DCs.ParseSnpTestGWAOutput(os.path.join(Arguments.SnpTestOutputPath,File),
                                      Log)
            DCsList.List.append(DCs)

        OutFileName = ''
        for S in Files[0].split('_'):
            if(re.match('CHR',S)):
                continue
            OutFileName += S
            OutFileName += '_'
        OutFileName = re.sub('.gz_','.gz',OutFileName)
        fw          = gzip.open(OutFileName,'wb')
        DCsList.WriteBioCratesGWAOutput(FH=fw,
                                        Log=Log)
        fw.close()

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
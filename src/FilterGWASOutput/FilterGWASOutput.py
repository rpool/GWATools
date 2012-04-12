#! /usr/bin/env python
import os
import re

import ArgumentParser
import Logger
import ParseSnpTestOutput

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
#    for p in range(162,Arguments.NPhe):
        P     = '_PHE'+str(p+1)+'_'
#        for c in range(1):
        for c in range(Arguments.NChr):
            C = '_CHR'+str(c+1)+'_'
            for File in SnpTestOutputFiles:
                if(re.search(P,File) and
                   re.search(C,File)):
                    ParseSnpTestOutput.Split(Log=Log,
                                             Arguments=Arguments,
                                             FileName=os.path.join(Arguments.SnpTestOutputPath,File))

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
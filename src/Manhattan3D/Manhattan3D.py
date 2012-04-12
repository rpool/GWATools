#! /usr/bin/env python
import os
import re
import scipy

import ArgumentParser
import Logger

iLARGE = 1e500

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

    if(Arguments.YProperty=='PHE'):
        XPath       = os.path.join(Arguments.SnpTestPath,Arguments.XProperty)
        XListDir    = os.listdir(XPath)
        MinXSpacing = iLARGE
        XMin        = None
        XMax        = 0
        for p in range(1): # if XProperty=='pos', all phenotypes have the same pos file content.
            P = 'PHE'+str(p+1)+'_'
            for c in range(Arguments.NChr):
                C = 'CHR'+str(c+1)+'_'
                for File in XListDir:
                    X = []
                    if(re.search(C+P,File)):
                        fr   = open(os.path.join(XPath,File),'r')
                        FMem = []
                        for Line in fr.readlines():
                            FMem.append(int(Line.strip().split()[0]))
                        fr.close()
                        for i in range(1,len(FMem)):
                            MinXSpacing = min(MinXSpacing,FMem[i]-FMem[i-1])
                        if(c==0):
                            XMin = min(FMem)
                        X.extend((scipy.array(FMem)+XMax))
                        XMax += max(FMem)
                        del FMem
        print XMin,XMax,MinXSpacing,max(X)
        YMin        = 1
        YMax        = Arguments.NPhe
        MinYSpacing = 1
        for p in range(Arguments.NPhe): # if XProperty=='pos', all phenotypes have the same pos file content.
            P = 'PHE'+str(p+1)+'_'
            for c in range(Arguments.NChr):
                C = 'CHR'+str(c+1)+'_'


    else:
        print '!! NOT IMPLEMENTED YET !!'

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
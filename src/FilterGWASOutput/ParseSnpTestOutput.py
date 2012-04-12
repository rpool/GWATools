import argparse
import re
import gzip
import os

import Logger

def Split(Log=Logger,
          Arguments=argparse.Namespace,
          FileName=str):
    LogString = '**** Parsing snptest output file \"'+FileName+'\" ...'
    print LogString
    Log.Write(LogString+'\n')

    fr = None
    if(re.search('.gz',FileName)):
        fr = gzip.open(FileName,'r')
    else:
        fr = open(FileName,'r')

    Header      = fr.readline()
    CountColumn = 0
    Name2Column = {}
    for Name in Header.strip().split():
        for ColumnName in Arguments.ParseArguments:
            for Entry in Name.split('_'):
                if(re.match(ColumnName,Entry) and
                   len(Entry)==len(ColumnName)):
                    Name2Column[ColumnName] = CountColumn
                    break
        CountColumn                  += 1

    Name2Path = {}
    for Name in Name2Column.iterkeys():
        Path = os.path.join(os.getcwd(),Name)
        Name2Path[Name] = Path
        if(not os.path.exists(Path)):
            os.mkdir(Path)

    FileHandles = {}
    for Name,Path in Name2Path.iteritems():
        BaseName = os.path.basename(FileName)
        C        = None
        P        = None
        for Entry in BaseName.split('_'):
            if(re.match('CHR',Entry)):
                C = Entry
            if(re.match('PHE',Entry)):
                P = Entry
        FName = os.path.join(Path,C+'_'+P+'_'+Name+'.dat')
        FileHandles[Name] = open(FName,'w')

    for Line in fr:
        LSplit = Line.strip().split()
        for Name,Column in Name2Column.iteritems():
            FileHandles[Name].write(LSplit[Column]+'\n')

    for FH in FileHandles.itervalues():
        FH.close()

    if(type(fr)==file):
        fr.close()

    return

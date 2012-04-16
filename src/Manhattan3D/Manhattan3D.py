#! /usr/bin/env python
import os
import sys
import re
import scipy
import pylab
import matplotlib

import ArgumentParser
import Logger

iLARGE = 1e500
fLARGE = 1.0e500

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
        X           = []
        for p in range(1): # if XProperty=='pos', all phenotypes have the same pos file content.
            P = 'PHE'+str(p+1)+'_'
            for c in range(Arguments.NChr):
                C = 'CHR'+str(c+1)+'_'
                for File in XListDir:
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
        LogString = '**** Parsed x-axis properties ...'
        print LogString
        Log.Write(LogString+'\n')

        YMin        = 1
        YMax        = Arguments.NPhe
        MinYSpacing = 1
        Y           = []
        for y in range(YMax):
            Y.append(y+1)
        LogString = '**** Processed y-axis properties ...'
        print LogString
        Log.Write(LogString+'\n')

        ZMin        = 0.0
        ZMax        = -fLARGE
        ZPath       = os.path.join(Arguments.SnpTestPath,Arguments.ZProperty)
        ZListDir    = os.listdir(ZPath)
        if(Arguments.boReadZExtrFromFile):
            LogString = '**** Reading z-axis extrema from file \"'+os.path.join(ZPath,'Extrema.dat')+'\" ...'
            print LogString
            Log.Write(LogString+'\n')
            fr    = open(os.path.join(ZPath,'Extrema.dat'),'r')
            LSplt = fr.readline().strip().split()
            fr.close()
            ZMin = float(LSplt[0])
            ZMax = float(LSplt[1])
        else:
            for p in range(Arguments.NPhe): # Scan for the maximum value of Z for the colorbar
                P = 'PHE'+str(p+1)+'_'
                Z = []
                for c in range(Arguments.NChr):
                    C    = 'CHR'+str(c+1)+'_'
                    File = os.path.join(ZPath,C+P+Arguments.ZProperty+'.dat')
                    fr   = None
                    if(os.path.basename(File) in ZListDir):
                        fr = open(File,'r')
                        for Line in fr:
                            Value = Line.strip()
                            if((Value!='-1') or
                               (not re.search('nan',Value))):
                                Z.append(float(Value))
                            else:
                                Z.append(1.0)
                        fr.close()
                Z    = scipy.array(Z)
                ZMax = max(ZMax,scipy.real(-scipy.log10(Z)).max())
                del Z
                LogString = '**** Determining maximal z-axis value, now at '+re.sub('_','',P)+', ZMax = '+str(ZMax)+' ...'
                print LogString
                Log.Write(LogString+'\n')
            LogString = '**** Writing z-axis extrema to file \"'+os.path.join(ZPath,'Extrema.dat')+'\" ...'
            print LogString
            Log.Write(LogString+'\n')
            fw = open(os.path.join(ZPath,'Extrema.dat'),'w')
            fw.write(str(ZMin)+' '+str(ZMax)+'\n')
            fw.close()

        LogString = '**** Generating 3D-Manhattan plot ...'
        print LogString
        Log.Write(LogString+'\n')

#       Lay-out stuff
        figwidth_pt   = 1422.0 # pt (from revtex \showthe\columnwidth)
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

        pylab.rcParams.update(params)

        PylabFigure = pylab.figure()
        PylabFigure.clf()

        Rectangle   = [left, bottom, width, height]
        PylabAxis   = PylabFigure.add_axes(Rectangle)
#        PylabAxis.set_xlabel(XLabel)
#        PylabAxis.set_ylabel(YLabel)
        Values = pylab.ones(shape=(10,len(X)),dtype=float) # indices run from 1 in data file!
        X             = scipy.array(X)
        print len(X)
        Y             = scipy.array(Y)
#        Extent        = [X.min()-0.5,X.max()+0.5,X.min()-0.5,X.max()+0.5]
#        Extent        = [X.min()-0.5,X.max()+0.5,Y.min()-0.5,Y.max()+0.5]
        CMap          = pylab.cm.get_cmap(name='jet',
                                          lut=None)
        PylabImAxis   = PylabFigure.add_axes(Rectangle)
        PylabImage    = PylabImAxis.imshow(Values,
#                                           extent=Extent,
                                           interpolation='nearest',
                                           cmap=CMap,
                                           origin='lower')


        LogString = '**** Writing plot to \"HeatMap.png\" ...'
        print LogString
        Log.Write(LogString+'\n')

#        PylabImAxis.set_xlim(Extent[0:2])
#        PylabAxis.set_xlim(Extent[0:2])
#        PylabImAxis.set_ylim(Extent[2:4])
#        PylabAxis.set_ylim(Extent[2:4])

        PylabColorBar = pylab.colorbar(PylabImage)
        PylabColorBar.set_label(r'$-{\rm log_{10}}(p-{\rm value})$')

        pylab.savefig('HeatMap.png')
#        pylab.show()
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
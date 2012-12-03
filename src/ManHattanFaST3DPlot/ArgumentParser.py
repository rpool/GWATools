import argparse
import os

import Logger

def LogArguments(Log=Logger,
                 ArgParser=argparse.ArgumentParser,
                 Arguments=argparse.Namespace):
    ArgParser.print_help()
    ArgParser.print_help(Log.GetFileHandle())

#   Calculate max. of keylength for formatting
    MaxLen = 0
    for Key in vars(Arguments).iterkeys():
        MaxLen = max(MaxLen,len(Key))
    LogString =  '\n****\n'+\
                 'Used arguments:\n'+\
                 '---------------'
    print LogString
    Log.Write(LogString+'\n')

    FormatString = '{:<'+str(MaxLen)+'}'
    LogString    = ''
    for Key,Value in vars(Arguments).iteritems():
        LogString += FormatString.format(Key)+': '+str(Value)+'\n'
    LogString += '****\n'
    print LogString
    Log.Write(LogString+'\n')
    return

def ParseArguments(Log=None):
    ArgumentParser = argparse.ArgumentParser(description=\
                                             'This python module can be used for displaying GWA output data in 3D.')
    ArgumentParser.add_argument('-p',
                                '--snptestpath',
                                dest='GWAOutPath',
                                help='PATH: Name of file path of the GWA output files (input)',
                                metavar='PATH',
                                default=os.path.join(os.getcwd(),'SnptestGWAOutput'))
    ArgumentParser.add_argument('-O',
                                '--outputtype',
                                dest='GWAOutputType',
                                help='NAME: Output type (e.g. fast,snptest,plink) (input)',
                                metavar='NAME',
                                default='snptest')
    ArgumentParser.add_argument('-B',
                                '--BadSNPFile',
                                dest='BadSNPFile',
                                help='PATH: Name of file that lists the bad SNPs (input)',
                                metavar='PATH',
                                default='BadSNPs_NTRMRG3.txt')
    ArgumentParser.add_argument('-L',
                                '--PhenotypeListFile',
                                dest='PhenotypeListFile',
                                help='PATH: Name of file that lists the phenotypesbad (input)',
                                metavar='PATH',
                                default='PhenoTypeList.csv')
    ArgumentParser.add_argument('-I',
                                '--SNPInfoFile',
                                dest='SNPInfoFile',
                                help='PATH: Name of the SNP info file (input)',
                                metavar='PATH',
                                default='SNP_INFO_NTRMRG3.csv.gz')
    ArgumentParser.add_argument('-x',
                                '--xproperty',
                                dest='XProperty',
                                help='STRING: Property to be displayed on the x-axis (input)',
                                metavar='STRING',
                                default='pos')
    ArgumentParser.add_argument('-y',
                                '--yproperty',
                                dest='YProperty',
                                help='STRING: Property to be displayed on the y-axis (input)',
                                metavar='STRING',
                                default='PHE')
    ArgumentParser.add_argument('-z',
                                '--zproperty',
                                dest='ZProperty',
                                help='STRING: Property to be displayed on the z-axis (input)',
                                metavar='STRING',
                                default='pvalue')
    ArgumentParser.add_argument('-M',
                                '--metaboliteclassesfile',
                                dest='MetabolitClassesFileName',
                                help='STRING: Name of the file that contains the metabolite classes (input)',
                                metavar='STRING',
                                default='MetaboliteClasses.txt')
    ArgumentParser.add_argument('-P',
                                '--nphenotypes',
                                dest='NPhe',
                                type=int,
                                help='INT: Number of phenotypes (input)',
                                metavar='INT',
                                default=163)
    ArgumentParser.add_argument('-C',
                                '--nchromosomes',
                                dest='NChr',
                                type=int,
                                help='INT: Number of chromosomes (input)',
                                metavar='INT',
                                default=22)
    ArgumentParser.add_argument('-Z',
                                '--readzextr',
                                dest='boReadZExtrFromFile',
                                help='FLAG: Read z-axis extrema from file  (input)',
                                action='store_true',
                                default=False)
    ArgumentParser.add_argument('-G',
                                '--greyscale',
                                dest='boGreyScale',
                                help='FLAG: Generate Manhattan plots in greyscale  (input)',
                                action='store_true',
                                default=False)

    Arguments = ArgumentParser.parse_args()

    return ArgumentParser,\
           Arguments

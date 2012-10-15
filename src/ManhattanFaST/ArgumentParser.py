import argparse

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

    FormatString = '{0:<'+str(MaxLen)+'}'
    LogString    = ''
    for Key,Value in vars(Arguments).iteritems():
        LogString += FormatString.format(Key)+': '+str(Value)+'\n'
    LogString += '****\n'
    print LogString
    Log.Write(LogString+'\n')
    return

def ParseArguments(Log=None):
    ArgumentParser = argparse.ArgumentParser(description=\
                                             'This python module can be used for displaying GWA output data.')
    ArgumentParser.add_argument('-s',
                                '--fastoutputfile',
                                dest='FaSTOutputFile',
                                help='FILENAME: Name of output file of the fastlmm run (input)',
                                metavar='FILENAME')
    ArgumentParser.add_argument('-i',
                                '--snpinfofile',
                                dest='SnpInfoFile',
                                help='FILENAME: Name of SNP info file (input)',
                                metavar='FILENAME')
    ArgumentParser.add_argument('-p',
                                '--fastoutputpath',
                                dest='FaSTOutputPath',
                                help='PATH: Name of output file path of the fastlmm run (input)',
                                metavar='PATH')
    ArgumentParser.add_argument('-e',
                                '--fastoutputpreext',
                                dest='FaSTOutputPreExtStr',
                                help='STRING: Pre-extension string of the fastlmm output files (input)',
                                metavar='STRING')
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
    ArgumentParser.add_argument('-H',
                                '--nchunks',
                                dest='NChunks',
                                type=int,
                                help='INT: Number of chunks into which the genotype data was divided (input)',
                                metavar='INT',
                                default=70)
    ArgumentParser.add_argument('-G',
                                '--greyscale',
                                dest='boGreyScale',
                                help='FLAG: Generate Manhattan plots in greyscale  (input)',
                                action='store_true',
                                default=False)

    Arguments = ArgumentParser.parse_args()

    return ArgumentParser,\
           Arguments
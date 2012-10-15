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
                                             'This python module can be used for filtering GWA output data.')
    ArgumentParser.add_argument('-p',
                                '--snptestoutputpath',
                                dest='SnpTestOutputPath',
                                help='PATH: Name of output file path of the snptest run (input)',
                                metavar='PATH')
    ArgumentParser.add_argument('-e',
                                '--snptestoutputpreext',
                                dest='SnpOutputPreExtStr',
                                help='STRING: Pre-extension string of the snptest output files (input)',
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
    ArgumentParser.add_argument('-A',
                                '--parseargs',
                                dest='ParseArguments',
                                help='LIST: Parse snptest output files (input)',
                                metavar='LIST',
                                nargs='+',
                                type=str)

    Arguments = ArgumentParser.parse_args()

    return ArgumentParser,\
           Arguments
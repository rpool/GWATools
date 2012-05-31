import re
import gzip
import scipy
import sys

import Logger

class DataContainer:
    def __init__(self):
        self.DataName  = None
        self.DataArray = None
        return

    def SetDataName(self,
                    Name=str):
        self.DataName = Name
        return

    def GetDataName(self):
        return self.DataName

    def InitDataArray(self):
        self.DataArray = []
        return

    def AppendToArray(self,
                      Entry=str):
        self.DataArray.append(Entry)
        return

    def GetDataArray(self):
        return self.DataArray


class DataContainers:
    def __init__(self):
        self.Name2Column    = {}
        self.Column2Name    = {}
        self.DataContainers = {}
        self.Label          = ''
        return

    def ParseSnpTestGWAOutput(self,
                              FileName=str,
                              Log=Logger):
        LogString = '**** Parsing snptest output file \"'+FileName+'\" ...'
        print LogString
        Log.Write(LogString+'\n')
        Log.GetFileHandle().flush()

        for Entry in FileName.split('_'):
            if(re.search('CHR',Entry)):
                self.Label = Entry

        fr = None
        if(re.search('.gz',FileName)):
            fr = gzip.open(FileName,'r')
        else:
            fr = open(FileName,'r')

        Header      = fr.readline()
        CountColumn = 0
        for Name in Header.strip().split():
            self.DataContainers[Name]     = DataContainer()
            self.Column2Name[CountColumn] = Name
            self.Name2Column[Name]        = CountColumn
            self.DataContainers[Name].SetDataName(Name)
            self.DataContainers[Name].InitDataArray()
            CountColumn                  += 1
        for Line in fr:
            LSplit = Line.strip().split()
            for i in range(len(LSplit)):
                Entry = LSplit[i]
                Name  = self.Column2Name[i]
                self.DataContainers[Name].AppendToArray(Entry)

        if(type(fr)==file):
            fr.close()

        return

class ListDataContainers:
    def __init__(self):
        self.List                         = []
        self.PhenotypeName                = ''
        self.HeaderList                   = None
        self.ColumnwidthList              = None
        self.ColumnIndexDict              = None
        self.HeaderName2SnpTestHeaderName = None
        self.FromExtArray                 = None
        self.AFCodedAllArray              = None
        self.NTotArray                    = None
        self.Name2SnpTestHeaderName       = None
        return

    def SetName2SnpTestHeaderName(self):
        self.Name2SnpTestHeaderName         = {}
        self.Name2SnpTestHeaderName['AA']   = 'cohort_1_AA'
        self.Name2SnpTestHeaderName['AB']   = 'cohort_1_AB'
        self.Name2SnpTestHeaderName['BB']   = 'cohort_1_BB'
        self.Name2SnpTestHeaderName['NULL'] = 'cohort_1_NULL'
        return

    def GetName2SnpTestHeaderName(self):
        if(self.Name2SnpTestHeaderName==None):
            self.SetName2SnpTestHeaderName()
        return self.Name2SnpTestHeaderName

    def SetHeaderName2SnpTestHeaderName(self):
        self.HeaderName2SnpTestHeaderName                  = {}
        self.HeaderName2SnpTestHeaderName['SNPID']         = 'rsid'
        self.HeaderName2SnpTestHeaderName['chr']           = 'chromosome'
        self.HeaderName2SnpTestHeaderName['position']      = 'pos'
        self.HeaderName2SnpTestHeaderName['coded_all']     = 'allele_B'
        self.HeaderName2SnpTestHeaderName['noncoded_all']  = 'allele_A'
        self.HeaderName2SnpTestHeaderName['strand_genome'] = 'FROMEXT'
        self.HeaderName2SnpTestHeaderName['beta']          = 'score_beta'
        self.HeaderName2SnpTestHeaderName['SE']            = 'score_se'
        self.HeaderName2SnpTestHeaderName['pval']          = 'score_pvalue'
        self.HeaderName2SnpTestHeaderName['AF_coded_all']  = 'CALCULATE AFCODEDALL'
        self.HeaderName2SnpTestHeaderName['HWE_pval']      = 'cohort_1_hwe'
        self.HeaderName2SnpTestHeaderName['n_total']       = 'CALCULATE NTOT'
        self.HeaderName2SnpTestHeaderName['imputed']       = 'FROMEXT'
        self.HeaderName2SnpTestHeaderName['used_for_imp']  = 'FROMEXT'
        self.HeaderName2SnpTestHeaderName['oevar_imp']     = 'info'
        return

    def GetHeaderName2SnpTestHeaderName(self):
        if(self.HeaderName2SnpTestHeaderName==None):
            self.SetHeaderName2SnpTestHeaderName()
        return self.HeaderName2SnpTestHeaderName

    def SetColumwidthList(self):
        self.ColumnwidthList = []
        MaxWidth             = 0
        for Entry in self.GetHeaderList():
            MaxWidth = max(len(Entry),MaxWidth)

        for Entry in self.GetHeaderList():
            self.ColumnwidthList.append(MaxWidth+1)

        return

    def GetColumnwidthList(self):
        if(self.ColumnwidthList==None):
            self.SetColumwidthList()
        return self.ColumnwidthList

    def SetHeaderList(self):
        self.HeaderList = []
        self.HeaderList.append('SNPID')
        self.HeaderList.append('chr')
        self.HeaderList.append('position')
        self.HeaderList.append('coded_all')
        self.HeaderList.append('noncoded_all')
        self.HeaderList.append('strand_genome')
        self.HeaderList.append('beta')
        self.HeaderList.append('SE')
        self.HeaderList.append('pval')
        self.HeaderList.append('AF_coded_all')
        self.HeaderList.append('HWE_pval')
        self.HeaderList.append('n_total')
        self.HeaderList.append('imputed')
        self.HeaderList.append('used_for_imp')
        self.HeaderList.append('oevar_imp')
        return

    def GetHeaderList(self):
        if(self.HeaderList==None):
            self.SetHeaderList()
        return self.HeaderList

    def SetPhenotypeName(self,
                         Name=str):
        self.PhenotypeName = Name
        return

    def GetPhenotypeName(self):
        return self.PhenotypeName

    def WriteHeader(self,
                    FH=file):
        ColumnWidthList = self.GetColumnwidthList()
        HeaderList      = self.GetHeaderList()
        for i in range(len(HeaderList)):
            Entry        = HeaderList[i]
            FormatString = '{:>'+str(ColumnWidthList[i])+'}'
            FH.write(FormatString.format(Entry))
        FH.write('\n')
        return

    def WriteBioCratesGWAOutput(self,
                                FH=file,
                                Log=Logger):
        for Entry in self.List:
            CheckList    = []
            for Value in Entry.DataContainers.itervalues():
                CheckList.append(len(Value.GetDataArray()))
            CheckList = list(set(CheckList))
            if(len(CheckList)!=1):
                LogString  = '**** ERROR: Column lengths of data arrays incosistent ! \n'
                LogString += '     EXITING ...'
                print LogString
                Log.Write(LogString+'\n')
                sys.exit(1)

        LogString = '**** Writing GWA results to \"'+FH.name+'\" ...'
        print LogString
        Log.Write(LogString+'\n')
        Log.GetFileHandle().flush()

        self.WriteHeader(FH)
        HeaderList      = self.GetHeaderList()
        ColumnWidthList = self.GetColumnwidthList()
        for DCs in self.List:
            for Value in self.GetColumnIndicesFromDCs().itervalues():
                if(Value=='CALCULATE AFCODEDALL'):
                    self.SetAFCodedAll(DCs=DCs)
                if(Value=='CALCULATE NTOT'):
                    self.SetNTot(DCs=DCs)
                if(Value=='FROMEXT'):
                    self.SetFromExt(DCs=DCs)

            ArrayLenth = len(DCs.DataContainers[self.GetHeaderName2SnpTestHeaderName()['chr']].GetDataArray())
            for i in range(ArrayLenth):
                for j in range(len(HeaderList)):
                    Entry        = HeaderList[j]
                    DCsColumn    = self.GetColumnIndicesFromDCs()[Entry]
                    String       = None
                    if(type(DCsColumn)==str):
                        if(DCsColumn=='CALCULATE AFCODEDALL'):
                            String = str(round(self.GetAFCodedAll(DCs=DCs)[i],8))
                        if(DCsColumn=='CALCULATE NTOT'):
                            String = str(int(round(self.GetNTot(DCs=DCs)[i])))
                        if(DCsColumn=='FROMEXT'):
                            String = self.GetFromExt(DCs=DCs)[i]
                    else:
                        Key    = DCs.Column2Name[DCsColumn]
                        String = DCs.DataContainers[Key].GetDataArray()[i]
                    FormatString = '{:>'+str(ColumnWidthList[j])+'}'
                    if(re.search('nan',String)):
                        String = 'NA'
                    elif(String=='-1'):
                        String = 'NA'
                    FH.write(FormatString.format(String))
                FH.write('\n')

            for Value in self.GetColumnIndicesFromDCs().itervalues():
                if(Value=='CALCULATE AFCODEDALL'):
                    self.PurgeAFCodedAll()
                if(Value=='CALCULATE NTOT'):
                    self.PurgeNTot()
                if(Value=='FROMEXT'):
                    self.PurgeFromExt()
        return

    def SetColumnIndicesFromDCs(self):
        self.ColumnIndexDict = {}
        for Name in self.GetHeaderList():
            SearchRegExp = self.GetHeaderName2SnpTestHeaderName()[Name]
            Index = None
            if(self.List[0].Name2Column.has_key(SearchRegExp)):
                Index = self.List[0].Name2Column[SearchRegExp]
            else:
                for DCsName,DCsIndex in self.List[0].Name2Column.iteritems():
                    if(re.search(SearchRegExp,DCsName)):
                        Index = DCsIndex
                if(Index==None):
                    Index = SearchRegExp
            self.ColumnIndexDict[Name] = Index
        return

    def GetColumnIndicesFromDCs(self):
        if(self.ColumnIndexDict==None):
            self.SetColumnIndicesFromDCs()
        return self.ColumnIndexDict

    def SetFromExt(self,
                   DCs=DataContainers):
        self.FromExtArray = []
        for i in range(len(DCs.DataContainers[self.GetHeaderName2SnpTestHeaderName()['chr']].GetDataArray())):
            self.FromExtArray.append('NA')
        return

    def GetFromExt(self,
                   DCs=DataContainers):
        if(self.FromExtArray==None):
            self.SetFromExt(DCs=DCs)
        return self.FromExtArray

    def PurgeFromExt(self):
        del self.FromExtArray
        self.FromExtArray = None
        return

    def SetAFCodedAll(self,
                      DCs=DataContainers):
        self.AFCodedAllArray  = scipy.array(DCs.DataContainers[self.GetName2SnpTestHeaderName()['AB']].GetDataArray()).astype(float)
        self.AFCodedAllArray += (scipy.array(DCs.DataContainers[self.GetName2SnpTestHeaderName()['BB']].GetDataArray()).astype(float)*2.0)
        self.AFCodedAllArray /= (scipy.array(self.GetNTot(DCs))*2.0)
        self.AFCodedAllArray  = list(self.AFCodedAllArray)
        return

    def GetAFCodedAll(self,
                      DCs=DataContainers):
        if(self.AFCodedAllArray==None):
            self.SetAFCodedAll(DCs=DCs)
        return self.AFCodedAllArray

    def PurgeAFCodedAll(self):
        del self.AFCodedAllArray
        self.AFCodedAllArray = None
        return

    def SetNTot(self,
                DCs=DataContainers):
        self.NTotArray  = scipy.array(DCs.DataContainers[self.GetName2SnpTestHeaderName()['AA']].GetDataArray()).astype(float)
        self.NTotArray += scipy.array(DCs.DataContainers[self.GetName2SnpTestHeaderName()['AB']].GetDataArray()).astype(float)
        self.NTotArray += scipy.array(DCs.DataContainers[self.GetName2SnpTestHeaderName()['BB']].GetDataArray()).astype(float)
        #=======================================================================
        ##
        ## Since cohort_NULL can be larger than zero due to missing phenotype or
        ## missing covariates in addition to missing genotype data, we decided not
        ## to add the 'NULL' value
        ##
        # self.NTotArray += scipy.array(DCs.DataContainers[self.GetName2SnpTestHeaderName()['NULL']].GetDataArray()).astype(float)
        #=======================================================================
        self.NTotArray  = list(self.NTotArray)
        return

    def GetNTot(self,
                DCs=DataContainers):
        if(self.NTotArray==None):
            self.SetNTot(DCs=DCs)
        return self.NTotArray

    def PurgeNTot(self):
        del self.NTotArray
        self.NTotArray = None
        return
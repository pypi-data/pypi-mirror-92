#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20180226
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import numpy as np
import os
from glob import glob
from imp import load_source
from itertools import combinations
from klusta.kwik import KwikModel

from sciscripts.Analysis import Analysis
from sciscripts.Analysis.Units import Units
from sciscripts.IO import IO, Klusta


## Level 0 -  Detection and clustering
def GetExpGroups(Exps):
    ExpGroups = []

    while Exps:
        print('-1: Run each separately')
        print('0: All at once')
        for E, Exp in enumerate(Exps): print(str(E+1)+':', Exp)
        print(str(len(Exps)+1)+': Discard remaining experiments')
        print('\n', 'You can run all folders separately,',
              '\n', 'run all as one single experiment or',
              '\n', 'group folders you want by index, comma separated.')

        FGroup = input('Choose folders to group: ')
        FGroup = [int(_) for _ in FGroup.split(',')]
        if len(FGroup) == 1:
            if FGroup[0] == -1:
                for _ in Exps: ExpGroups.append([_])
                Exps = []; break

            elif FGroup[0] == 0:
                ExpGroups.append(Exps)
                Exps = []; break

            elif FGroup[0] == len(Exps)+1:
                Exps = []; break

            else:
                FGroup = [Exps[FGroup[0]-1]]
                ExpGroups.append(FGroup); Exps.remove(FGroup[0])

        else:
            FGroup = [Exps[F-1] for F in FGroup]
            ExpGroups.append(FGroup)
            for F in FGroup: Exps.remove(F)

    return(ExpGroups)


def ClusterizeSpks(Folders, ProbeSpacing=50, Log=None, **Kws):
    if not Log: Log = {K: [] for K in ['Done', 'Errors', 'ErrorsLog', 'Skipped']}
    LogFile = os.environ['ANALYSISPATH']+'/ClusterizeSpks-Last.dict'

    for Folder in Folders:
        # try:
        if Folder in Log['Done']+Log['Errors']+Log['Skipped']: continue

        ExpFolder = os.environ['ANALYSISPATH']+'/'+'/'.join(Folder.split('/')[-2:]) + '/KlustaFiles'
        os.makedirs(ExpFolder, exist_ok=True)

        ExpName = Folder.split('/')[-2]
        Exps = sorted(glob(Folder+'/*20??-*'))
        Exps = [_ for _ in Exps if '.dict' not in _
                                and 'Impedance' not in _
                                and '.hdf5' not in _
                                and 'BigOne' not in _] # Temp override

        # ExpGroups = GetExpGroups(Exps)
        ## Override
        ExpGroups = [Exps]
        if Folder+'/ExpGroups' in glob(Folder+'/*'):
            ExpGroups = IO.Txt.Read(Folder+'/ExpGroups')
            ExpGroups = [[Folder+'/'+_ for _ in F] for F in ExpGroups]

        for Es, Exps in enumerate(ExpGroups):
            FilesPrefix = ExpFolder+'/'+ExpName+'_Exp' + "{0:02d}".format(int(Es))

            if FilesPrefix+'.prm' not in glob(ExpFolder+'/*'):
                raw_data_files = []

                DataInfo = glob(Folder + '/*.dict')[0]
                DataInfo = IO.Txt.Read(DataInfo)

                if 'Probe' in DataInfo.keys():
                    if 'ChSpacing' in DataInfo['Probe']:
                        ProbeSpacing = DataInfo['Probe']['ChSpacing']

                    if DataInfo['Probe']['Remapped']:
                        PrbFile = os.environ['SCRIPTSPATH'] + \
                                  '/Python3/Klusta/A16-'+str(ProbeSpacing)+'.prb'
                    else:
                        PrbFile = FilesPrefix+'.prb'
                        ChannelMap = Analysis.RemapCh(DataInfo['Probe']['Probe'],
                                                          DataInfo['Probe']['Adaptor'])
                        ChannelMap = [_-1 for _ in ChannelMap]

                        Klusta.PrbWrite(PrbFile, ChannelMap, ProbeSpacing)
                else:
                    print('No probe info saved. Skip remap...')
                    PrbFile = os.environ['SCRIPTSPATH'] + '/Python3/Klusta/A16-'+str(ProbeSpacing)+'.prb'


                for E, Exp in enumerate(Exps):
                    FilesExt = [F.split('.')[-1] for F in glob(Exp+'/*.*')]
                    ChNo, Proc = IO.OpenEphys.GetChNoAndProcs(Exp+'/settings.xml')

                    if FilesExt == ['xml'] or 'dat' in FilesExt:
                        Files = sorted(glob(Exp+'/**/*.dat', recursive=True))
                        if 'experiment' in Files[0]:
                            Files = sorted(Files, key=lambda x: int(x.split('/')[-4][9:]))

                        raw_data_files += Files

                        Rate = IO.OpenEphys.SettingsXML.GetSamplingRate(Exp+'/settings.xml')
                        DType = 'int16'

                    else:
                        print('Loading', Exp, '...')
                        Data, Rate = IO.DataLoader(Exp, 'Bits')
                        # RecChMap = (np.arange(16)).tolist()+[DataInfo['DAqs']['StimCh']-1,DataInfo['DAqs']['TTLCh']-1]

                        for R, Rec in sorted(Data[Proc].items(), key=lambda i: int(i[0])):
                            Rec = Rec[:,np.arange(16)]
                            DataFile = ''.join([ExpName, '_Exp', "{0:02d}".format(int(Es)),
                                               '-', "{0:02d}".format(int(E)), '_Rec',
                                               "{0:02d}".format(int(R))])
                            RawDataInfo = {'Rate': Rate[Proc], 'Shape': Rec.shape, 'DType': str(Rec.dtype)}
                            if not ExpFolder+'/'+DataFile+'.dat' in glob(ExpFolder+'/*'):
                                print('Writing', DataFile, '...')
                                IO.Bin.Write(Rec, ExpFolder+'/'+DataFile+'.dat', RawDataInfo)

                            raw_data_files.append(ExpFolder+'/'+DataFile+'.dat')

                        ChNo = RawDataInfo['Shape'][1]
                        Rate = int(RawDataInfo['Rate'])
                        DType = RawDataInfo['DType']
                        del(Data)

                if not False in [_ in Log['Errors'] for _ in Exps]:
                    continue

                DataInfo['RawData'] = Exps

                Klusta.PrmWrite(FilesPrefix+'.prm', ExpName+'_Exp' + "{0:02d}".format(int(Es)),
                                PrbFile, raw_data_files, Rate, ChNo, DType,
                                DataInfo=DataInfo)

            # Klusta.Run(ExpName+'_Exp' + "{0:02d}".format(int(Es))+'.prm',
            #            ExpFolder, Overwrite=True)

        Log['Done'].append(Folder)
        IO.Txt.Write(Log, LogFile)

        # except Exception as e:
        #     Log['Errors'].append(Folder)
        #     Log['ErrorsLog'].append(e)
        #     IO.Txt.Write(Log, LogFile)
        #     print(e)


## Level 1 - After detection and clustering
def GetAllClusters(PrmFile):
    AnalysisFile = '/'.join(PrmFile.split('/')[:-2]) + '/Units/'+ PrmFile.split('/')[-3]
    KwikFile = PrmFile[:-3]+'kwik'
    Exp = PrmFile.split('/')[-1][:-4]

    Clusters = KwikModel(KwikFile)
    Offsets = Clusters.all_traces.offsets
    Rate = Clusters.sample_rate
    RecLengths = [int(Offsets[_]/Rate-Offsets[_-1]/Rate) for _ in range(1,len(Offsets))]

    SpkTimes = Clusters.spike_times
    SpkClusters =  Clusters.spike_clusters
    SpkRecs =  Clusters.spike_recordings
    Waveforms = Clusters.all_waveforms

    ## Get info
    Prm = load_source('', PrmFile)
    Prb = load_source('', Prm.prb_file)
    ChSpacing = Prb.channel_groups['0']['geometry']
    ChSpacing = abs(ChSpacing[0][1] - ChSpacing[1][1])

    DataInfo = Prm.DataInfo
    DataInfo['Analysis'] = {}
    DataInfo['Analysis']['Channels'] = Clusters.probe.channels
    DataInfo['Analysis']['ChNoTotal'] = Prm.traces['n_channels']
    DataInfo['Analysis']['ChSpacing'] = ChSpacing
    DataInfo['Analysis']['ClusterRecs'] = Clusters.recordings
    DataInfo['Analysis']['ClusterLabels'] = Clusters.cluster_groups
    DataInfo['Analysis']['RecLengths'] = RecLengths
    DataInfo['Analysis']['RecOffsets'] = Offsets
    DataInfo['Analysis']['Rate'] = Clusters.sample_rate
    DataInfo['Analysis']['RawData'] = Prm.DataInfo['RawData']


    for K,V in DataInfo['ExpInfo'].items():
        if 'Hz' not in V.keys():
            DataInfo['ExpInfo'][K]['Hz'] = 'Baseline'

    ## Get recs
    Recs = Units.GetRecsNested(DataInfo)
    ClusterRecs = [b for a in Recs for b in a]

    if 'Prevention/20170803-Prevention_04-UnitRec/KlustaFiles/Prevention_Exp00.prm' in PrmFile:
        ClusterRecs = Clusters.recordings
        Recs += [np.array([5])]
        DataInfo['RawData'] = DataInfo['RawData'][:-1] + [DataInfo['RawData'][3]] + [DataInfo['RawData'][-1]]
        DataInfo['ExpInfo']['05'] = DataInfo['ExpInfo']['04']

    if ClusterRecs != Clusters.recordings:
        print('Wrong number of recordings! Cannot extract TTLs!')
        DataInfo['Analysis']['RecNoMatch'] = False
    else:
        DataInfo['Analysis']['RecNoMatch'] = True

    DataInfo['Analysis']['RecsNested'] = Recs

    IO.Bin.Write(Waveforms, AnalysisFile + '_' + Exp + '_AllClusters/Waveforms.dat')
    IO.Bin.Write(SpkTimes, AnalysisFile + '_' + Exp + '_AllClusters/SpkTimes.dat')
    IO.Bin.Write(SpkClusters, AnalysisFile + '_' + Exp + '_AllClusters/SpkClusters.dat')
    IO.Bin.Write(SpkRecs, AnalysisFile + '_' + Exp + '_AllClusters/SpkRecs.dat')
    IO.Txt.Write(DataInfo, AnalysisFile + '_' + Exp + '_AllClusters/Info.dict')

    return(None)


def GetCellsResponse(UnitRec, AnalysisFile='', Save=False, Return=True):
    CellsResponse = {}
    for K in ['SpkResp', 'SpkCount']:
        CellsResponse[K] = np.zeros(UnitRec['DV'].shape, dtype=np.float32)

    for U in range(UnitRec['UnitId'].shape[0]):
        PSTH = UnitRec['PSTH'][U]
        if 'str' in str(type(PSTH)):
            PSTH = IO.Bin.Read(PSTH)[0]

        TrialNo = PSTH.shape[1]
        if PSTH.sum() < TrialNo*0.03:
            # if too few spikes in PSTH
            CellsResponse['SpkResp'][U] = 1
            CellsResponse['SpkCount'][U] = 0
        else:
            CellsResponse['SpkResp'][U] = Units.SpkRespPVal(PSTH,
                                                      UnitRec['PSTHX'][:,U],
                                                      N=TrialNo)
            CellsResponse['SpkCount'][U] = Units.SpkResp(PSTH,
                                                       UnitRec['PSTHX'][:,U])

    if Save: IO.Bin.Write(CellsResponse, AnalysisFile)

    if Return:
        return(CellsResponse)
    else:
        del(CellsResponse)
        return(None)


def GetCellsChanges(Cells, Stims, StimRef, AnalysisFile, Save=True, Return=True):
    CellsChanges = {}

    for Stim in Stims:
        Ind = (Cells['StimType'] == Stim)
        CellsChanges[Stim] = Cells['MaxResp'][Ind]
        CellsChanges[Stim+'-Freqs'] = Cells['BestFreq'][Ind]
        CellsChanges[Stim+'-dBs'] = Cells['BestdB'][Ind]

    StimPairs = list(combinations(Stims,2))

    for Pair in StimPairs:
        if StimRef not in Pair: continue
        if Pair[-1] != StimRef: Pair = (Pair[1], Pair[0])

        Key = 'Vs'.join(Pair)
        ChangedFreq = CellsChanges[Pair[0]+'-Freqs'] != CellsChanges[Pair[1]+'-Freqs']
        ChangeddB = CellsChanges[Pair[0]+'-dBs'] != CellsChanges[Pair[1]+'-dBs']

        CellsChanges[Key] = ((CellsChanges[Pair[0]]/CellsChanges[Pair[1]])-1)*100
        CellsChanges[Key+'-FreqChangePerc'] = len(CellsChanges[Key][ChangedFreq])*100/len(CellsChanges[Key])
        CellsChanges[Key+'-dBChangePerc'] = len(CellsChanges[Key][ChangeddB])*100/len(CellsChanges[Key])

    if Save: IO.Bin.Write(CellsChanges, AnalysisFile)

    if Return:
        return(CellsChanges)
    else:
        del(CellsChanges)
        return(None)



def GetUnitsParameters(UnitRec, CellsResponse, AnalysisFile, Save=True, Return=True):
    UnitsId = np.unique(UnitRec['UnitId'])
    Stims = np.unique(UnitRec['StimType'])
    Intensities = np.unique(UnitRec['dB'])
    Freqs = sorted(np.unique(UnitRec['Freq']), key=lambda x: int(x.split('-')[0]))
    Freqs = np.array(Freqs)

    Cells = {
        'Freqs': Freqs,
        'Intensities': Intensities,
        'UnitId': np.zeros((Stims.size * UnitsId.size), dtype=UnitRec['UnitId'].dtype),
        'StimType': np.zeros((Stims.size * UnitsId.size), dtype=UnitRec['StimType'].dtype),
        'RespMax': np.zeros((Stims.size * UnitsId.size), dtype=CellsResponse['SpkResp'].dtype),
        'FreqMax': np.zeros((Stims.size * UnitsId.size), dtype=UnitRec['Freq'].dtype),
        'FreqBest': np.zeros((Intensities.size, Stims.size * UnitsId.size), dtype=UnitRec['Freq'].dtype),
        'FreqSharpness': np.zeros((Intensities.size, Stims.size * UnitsId.size), dtype='float32'),
        'dBMax': np.zeros((Stims.size * UnitsId.size), dtype=UnitRec['dB'].dtype),
        'dBBest': np.zeros((Freqs.size, Stims.size * UnitsId.size), dtype=UnitRec['dB'].dtype),
        'dBSharpness': np.zeros((Freqs.size, Stims.size * UnitsId.size), dtype='float32'),
        # 'dBLowest': np.zeros((Stims.size * UnitsId.size), dtype=UnitRec['dB'].dtype),
        'FR_HzdBStim': np.zeros((Intensities.size, Freqs.size, Stims.size * UnitsId.size), dtype='float32')
    }


    Invalid = []


    for U,Unit in enumerate(UnitsId):
        for S,Stim in enumerate(Stims):
            UInd = S + (len(Stims)*U)

            print('Unit', U, 'Stim', Stim)
            FreqdB = np.zeros((len(Intensities),len(Freqs)), dtype='float32')

            for I,Intensity in enumerate(Intensities):
                for F,Freq in enumerate(Freqs):
                    Ind = (
                        UnitRec['UnitId'] == Unit) * (
                        UnitRec['dB'] == Intensity) * (
                        UnitRec['Freq'] == Freq) * (
                        UnitRec['StimType'] == Stim
                    )

                    if not True in Ind:
                        FreqdB[I,F] = 0
                        continue

                    while UnitRec['FiringRate'][Ind].shape[0] > 1:
                        Ind[np.where((UnitRec['FiringRate'] == UnitRec['FiringRate'][Ind][1]))[0]] = False

                    FR = IO.Bin.Read(UnitRec['FiringRate'][Ind][0])[0]
                    FreqdB[I,F] = FR.mean()

            # Peak and sharpness
            FRPerFreqPerdB = Analysis.Normalize(FreqdB.T)
            FreqSharpness, FreqBest = FRPerFreqPerdB.mean(axis=0), Freqs[FRPerFreqPerdB.argmax(axis=0)]

            FRPerdBPerFreq = Analysis.Normalize(FreqdB)
            dBSharpness, dBBest = FRPerdBPerFreq.mean(axis=0), Intensities[FRPerdBPerFreq.argmax(axis=0)]

            RespMax = FreqdB.max()
            FreqMax = np.where((FreqdB == RespMax))
            # dBMin = FreqdB[:,FreqMax[1][0]].min()
            # dBMin =
            dBMax, FreqMax = Intensities[FreqMax[0][0]], Freqs[FreqMax[1][0]]



            Cells['UnitId'][UInd] = Unit
            Cells['StimType'][UInd] = Stim
            Cells['RespMax'][UInd] = RespMax
            Cells['FreqMax'][UInd] = FreqMax
            Cells['FreqBest'][:,UInd] = FreqBest
            Cells['FreqSharpness'][:,UInd] = FreqSharpness
            Cells['dBMax'][UInd] = dBMax
            Cells['dBBest'][:,UInd] = dBBest
            Cells['dBSharpness'][:,UInd] = dBSharpness
            Cells['FR_HzdBStim'][:,:,UInd] = FreqdB
            # Cells['dBLowest'][UInd] = dBMin

    ## Cleaning
    if Invalid:
        Invalid = [Cells['UnitId'] == I for I in Invalid]
        Invalid = np.sum(Invalid, axis=0, dtype=bool)
        ValidIds = (Cells['UnitId'] != 0) * ~Invalid
    else:
        ValidIds = (Cells['UnitId'] != 0)

    for Key in ['UnitId', 'StimType', 'RespMax', 'FreqMax', 'dBMax']:#, 'dBLowest']:
        Cells[Key] = Cells[Key][ValidIds]

    for Key in ['FreqBest', 'FreqSharpness', 'dBBest', 'dBSharpness']:
        Cells[Key] = Cells[Key][:,ValidIds]

    Cells['FR_HzdBStim'] = Cells['FR_HzdBStim'][:,:,ValidIds]

    if Save: IO.Bin.Write(Cells, AnalysisFile)

    if Return:
        return(Cells)
    else:
        del(Cells)
        return(None)


def QuantifyPerStim(AsdfFiles, Stims, Save=True, Return=True):
    Resp = {_: {'Total': 0} for _ in Stims}
    RespIDs = {_: [] for _ in Stims}

    for S, Stim in Stims:
        for AsdfFile in AsdfFiles:
            Preffix = AsdfFile.split('/')[-1][:-13]+'Unit'

            UnitRec = IO.Asdf.Load(AsdfFile)
            CellsResponse = IO.Asdf.Read('_'.join(AsdfFile.split('_')[:-1])+'_CellsResponse.asdf')
            StimIndex = UnitRec['StimType'] == Stim
            Resp[Stim]['Total'] += len(UnitRec['UnitId'][StimIndex])

            RS = (CellsResponse['SpkResp'] < 0.05) * StimIndex
            Resp[Stim]['Responsive'] = len(UnitRec['UnitId'][RS])
            for _ in UnitRec['UnitId'][RS]: RespIDs[Stim].append(Preffix+"{0:04d}".format(_))

    Preffix = os.path.commonprefix(AsdfFiles)
    if Save:
        IO.Txt.Write(Resp, Preffix+'_Resp.txt')
        IO.Txt.Write(RespIDs, Preffix+'_RespIDs.txt')

    if Return: return(Resp, RespIDs)


def UnitRecLoad(UnitFolder):
    UnitFiles = [_ for _ in glob(UnitFolder+'/*') if '.dat' in _ and 'Info' not in _]
    Keys = [_.split('/')[-1].split('.')[0] for _ in UnitFiles]
    UnitRec = {Key: IO.Bin.Read(UnitFiles[K])[0] for K, Key in enumerate(Keys)}

    UnitFiles = {
        K: [_ for _ in glob(UnitFolder+'/'+K+'/*') if 'Info' not in _]
        for K in ['PSTH', 'Raster', 'Spks', 'FiringRate']
    }

    UnitFiles = {
            K: np.array(sorted(V, key=lambda x: int(x.split('_')[-1].split('.')[0])))
            for K,V in UnitFiles.items()
    }

    # UnitRec['PSTH'] = [IO.Bin.Read(_)[0] for _ in UnitFiles['PSTH']]
    UnitRec = {**UnitRec, **UnitFiles}

    return(UnitRec)


## Level 1
def QuantifyPerOpsinPerStim(AsdfFiles, Save=True, Return=True):
    Resp = {_: {'Total': 0} for _ in AsdfFiles.keys()}
    RespIDs = {_: {} for _ in AsdfFiles.keys()}
    for O, Opsin in AsdfFiles.items():
        for K in ['Sound', 'SoundLight', 'LightMask']:
            Resp[O][K] = 0
            RespIDs[O][K] = []

        for AsdfFile in Opsin:
            Preffix = AsdfFile.split('/')[-1][:-13]+'Unit'
            print(Preffix)

            UnitRec = IO.Asdf.Read(AsdfFile)

            # CellsResponse = IO.Asdf.Read('_'.join(AsdfFile.split('_')[:-1])+'_CellsResponse.asdf')
            # CellsResponse = {'SpkResp': UnitRec['SpkResp']}
            CellsResponse = GetCellsResponse(UnitRec, '')

            BadUnits = len(CellsResponse['SpkResp'][CellsResponse['SpkResp'] == 1])
            Resp[O]['Total'] += len(np.unique(UnitRec['UnitId'])) - BadUnits

            RS = (CellsResponse['SpkResp'] < 0.05) * (UnitRec['StimType'] == 'Sound')
            RSL = (CellsResponse['SpkResp'] < 0.05) * (UnitRec['StimType'] == 'SoundLight')
            RS[CellsResponse['SpkResp'] == 1] = False
            RSL[CellsResponse['SpkResp'] == 1] = False

            SoundLight = UnitRec['UnitId'][RSL][np.isin(UnitRec['UnitId'][RSL], UnitRec['UnitId'][RS], invert=True)]
            LightMasked = UnitRec['UnitId'][RS][np.isin(UnitRec['UnitId'][RS], UnitRec['UnitId'][RSL], invert=True)]

            Resp[O]['LightMask'] += len(LightMasked)
            for _ in LightMasked: RespIDs[O]['LightMask'].append(Preffix+"{0:04d}".format(_))

            if 'Arch' not in O:
                RL = (CellsResponse['SpkResp'] < 0.05) * (UnitRec['StimType'] == 'Light')
                RL[CellsResponse['SpkResp'] == 1] = False

                if 'Light' not in Resp[O]: Resp[O]['Light'] = 0
                if 'Both' not in Resp[O]: Resp[O]['Both'] = 0
                if 'Light' not in RespIDs[O]: RespIDs[O]['Light'] = []
                if 'Both' not in RespIDs[O]: RespIDs[O]['Both'] = []

                SoundOnly = UnitRec['UnitId'][RS][np.isin(UnitRec['UnitId'][RS], UnitRec['UnitId'][RL], invert=True)]
                LightOnly = UnitRec['UnitId'][RL][np.isin(UnitRec['UnitId'][RL], UnitRec['UnitId'][RS], invert=True)]
                SoundLight = SoundLight[np.isin(SoundLight, UnitRec['UnitId'][RL], invert=True)]
                Both = np.intersect1d(UnitRec['UnitId'][RS],UnitRec['UnitId'][RL])


                Resp[O]['Sound'] += len(SoundOnly)
                Resp[O]['Light'] += len(LightOnly)
                Resp[O]['SoundLight'] += len(SoundLight)
                Resp[O]['Both'] += len(Both)

                for _ in SoundOnly: RespIDs[O]['Sound'].append(Preffix+"{0:04d}".format(_))
                for _ in LightOnly: RespIDs[O]['Light'].append(Preffix+"{0:04d}".format(_))
                for _ in SoundLight: RespIDs[O]['SoundLight'].append(Preffix+"{0:04d}".format(_))
                for _ in Both: RespIDs[O]['Both'].append(Preffix+"{0:04d}".format(_))

            else:
                Resp[O]['Sound'] += len(UnitRec['UnitId'][RS])
                Resp[O]['SoundLight'] += len(SoundLight)

                for _ in UnitRec['UnitId'][RS]: RespIDs[O]['Sound'].append(Preffix+"{0:04d}".format(_))
                for _ in SoundLight: RespIDs[O]['SoundLight'].append(Preffix+"{0:04d}".format(_))

        # Resp[O]['Fast'] =

        if 'Arch' in O:
            Resp[O]['Responsive'] = Resp[O]['Sound']+Resp[O]['SoundLight']
        else:
            Resp[O]['Responsive'] = Resp[O]['Sound']+Resp[O]['Light']+Resp[O]['SoundLight']+Resp[O]['Both']

    Preffix = os.path.commonprefix([_ for K in AsdfFiles.values() for _ in K])
    if Save:
        IO.Txt.Write(Resp, Preffix+'_Resp.txt')
        IO.Txt.Write(RespIDs, Preffix+'_RespIDs.txt')

    if Return: return(Resp, RespIDs)


def AllUnits(AnalysisPath, TimeWindow, ISISize=0.01, TTLCh=None, BinSize=None, AnalogTTLs=True, Save=True, **Kws):
    PrmFiles = sorted(glob(AnalysisPath+'/**/*.prm', recursive=True))
    for PrmFile in PrmFiles:
        UnitRec = GetAllUnits(PrmFile, TimeWindow, ISISize, TTLCh, BinSize, AnalogTTLs, Save)

        AnalysisPrefix = '/'.join(PrmFile.split('/')[:-2]) + '/Units/'+ PrmFile.split('/')[-3]
        Exp = PrmFile.split('/')[-1][:-4]
        AnalysisPrefix += '_' + Exp

        ## To load UnitRec from AnalysisFolder
        AnalysisFolder = AnalysisPrefix + '_AllUnits'
        # UnitRec = MergeUnits(UnitRec, AnalysisFolder, Save)
        UnitFiles = [_ for _ in glob(AnalysisFolder+'/*') if '.dat' in _ and 'Info' not in _]
        Keys = [_.split('/')[-1].split('.')[0] for _ in UnitFiles]
        UnitRec = {Key: IO.Bin.Read(UnitFiles[K])[0] for K, Key in enumerate(Keys)}

        UnitFiles = {
            K: [_ for _ in glob(AnalysisFolder+'/'+K+'/*') if 'Info' not in _]
            for K in ['PSTH', 'Raster', 'Spks', 'FiringRate']
        }

        UnitFiles = {
                K: sorted(V, key=lambda x: int(x.split('_')[-1].split('.')[0]))
                for K,V in UnitFiles.items()
        }

        # UnitRec['PSTH'] = [IO.Bin.Read(_)[0] for _ in UnitFiles['PSTH']]
        UnitRec = {**UnitRec, **UnitFiles}

        UnitsId = np.unique(UnitRec['UnitId'])
        Stims = np.unique(UnitRec['StimType'])
        Freqs = np.unique(UnitRec['Freq'])
        Intensities = np.unique(UnitRec['dB'])

        CellsResponse = GetCellsResponse(UnitRec.copy(), AnalysisPrefix + '_CellsResponse', Save)

        # ExtraInfo = {'SpkResp': CellsResponse['SpkResp']}
        # ExtraInfo = {}
        # KlPlot.Features(UnitRec, AnalysisPrefix+'_Plots', Exp, BinSize=None, ExtraInfo=ExtraInfo.copy(), Ext=['svg'], Save=False, Show=True)

        CellsParameters = GetUnitsParameters(UnitRec.copy(), CellsResponse.copy(), UnitsId, Stims, Freqs, Intensities, AnalysisPrefix + '_CellsParameters', Save)
        GetCellsChanges(CellsParameters.copy(), Stims, Stims[1], AnalysisPrefix + '_CellsChanges', Save, Return=False)

    AsdfFiles = sorted(glob(AnalysisPath+'/**/*_AllUnits.asdf'))
    QuantifyPerStim(AsdfFiles, Stims, Save, Return=False)

    AsdfFiles = sorted(glob(AnalysisPath+'/**/*_Cells.asdf'))
    AllCells = [IO.Asdf.Read(File) for File in AsdfFiles]

    TotalU = [np.unique(C['UnitId']) for C in AllCells]

    for C, Cell in enumerate(AllCells):

        if C == 0: NewUnitsId = np.arange(len(TotalU[C]))
        else: NewUnitsId = np.arange(len(TotalU[C])) + AllCells[C-1]['UnitId'][-1]+1

        for I, Id in enumerate(Cell['UnitId']):
            Ind = np.where(TotalU[C] == Id)[0][0]
            AllCells[C]['UnitId'][I] = NewUnitsId[Ind]

    Merge = {}
    for Key in AllCells[0].keys():
        if Key not in ['Intensities', 'Freqs']:
            Merge[Key] = np.concatenate([Cell[Key] for Cell in AllCells], axis=-1)

    Stims = np.unique(Merge['StimType'])
    GroupPath = os.path.commonprefix(AsdfFiles)+'_CellsChangesMerge.asdf'
    GetCellsChanges(Merge, Stims, Stims[-1], GroupPath, Save, Return=False)


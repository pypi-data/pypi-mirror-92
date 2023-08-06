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
def GetAllUnits(PrmFile, TimeWindow, ISISize=0.01, TTLCh=None, BinSize=None, AnalogTTLs=True, Save=True, Return=True, **Kws):
    AnalysisFile = '/'.join(PrmFile.split('/')[:-2]) + '/Units/'+ PrmFile.split('/')[-3]
    KwikFile = PrmFile[:-3]+'kwik'
    Exp = PrmFile.split('/')[-1][:-4]

    Clusters = KwikModel(KwikFile)
    Rate = np.array(Clusters.sample_rate)
    Offsets = Clusters.all_traces.offsets
    Good = [Id for Id,Key in Clusters.cluster_groups.items() if Key == 'good']

    if not Good:
        print('No good units in this file :(')
        return(None)

    RecLengths = [int(Offsets[_]/Rate-Offsets[_-1]/Rate) for _ in range(1,len(Offsets))]

    #== Verify noise units
    # RealGood = Good[:]
    # Good = [[Id,Key] for Id,Key in Clusters.cluster_groups.items() if Id not in RealGood]
    # GoodK = [_[1] for _ in Good]
    # Good = [_[0] for _ in Good]
    #==

    # Overrides - Good units in noise clusters
    if PrmFile == 'WHATEVER.prm': Good += [5,8,12,16,19,21,37,40,42]

    if not BinSize: BinSize = 1000/Rate
    PSTHX = np.arange(TimeWindow[0], TimeWindow[1], BinSize)
    RasterX = np.arange(PSTHX[0], PSTHX[-1], 1000/Rate)

    UnitRec = {}
    for K in ['UnitId', 'DV']: UnitRec[K] = np.zeros((len(Good)*len(Clusters.recordings)), dtype=np.int16)
    for K in ['dB']: UnitRec[K] = np.zeros((len(Good)*len(Clusters.recordings)), dtype=np.float32)
    for K in ['Freq', 'StimType']: UnitRec[K] = ['0' for _ in range(len(Good)*len(Clusters.recordings))]
    # for K in ['ISI', 'PSTH', 'Raster', 'Spks', 'FiringRate']: UnitRec[K] = [0 for _ in range(len(Good)*len(Clusters.recordings))]

    UnitRec['RMSs'] = np.zeros((len(Clusters.channels), len(Good)*len(Clusters.recordings)), dtype=np.float32)
    UnitRec['PSTHX'] = np.zeros((len(PSTHX),len(Good)*len(Clusters.recordings)), dtype=np.float32)
    UnitRec['RasterX'] = np.zeros((len(RasterX),len(Good)*len(Clusters.recordings)), dtype=np.float32)

    Prm = load_source('', PrmFile)
    Prb = load_source('', Prm.prb_file)
    Channels = Prb.channel_groups['0']['channels']

    if not TTLCh:
        TTLCh = Prm.DataInfo['DAqs']['TTLCh']
        # TTLCh = 0 # Temp override

    for K,V in Prm.DataInfo['ExpInfo'].items():
        if 'Hz' not in V.keys():
            Prm.DataInfo['ExpInfo'][K]['Hz'] = 'Baseline'

    if 'Probe' not in Prm.DataInfo.keys():
        Prm.DataInfo['Probe'] = {'ChSpacing': 50}


    Recs = [np.arange(len(Prm.DataInfo['Audio']['Intensities']))
            if V['Hz'] != 'Baseline' else np.array([0])
            for K,V in enumerate(Prm.DataInfo['ExpInfo'].values())]

    Recs = [len(_) for _ in Recs]

    Prev = 0
    for R,Rec in enumerate(Recs):
        Prev = Prev+len(Recs[R-1]) if R else 0
        Recs[R] = np.arange(Rec) + Prev

    ClusterRecs = [b for a in Recs for b in a]

    if 'Prevention/20170803-Prevention_04-UnitRec/KlustaFiles/Prevention_Exp00.prm' in PrmFile:
        ClusterRecs = Clusters.recordings
        Recs += [np.array([5])]
        Prm.DataInfo['RawData'] = Prm.DataInfo['RawData'][:-1] + [Prm.DataInfo['RawData'][3]] + [Prm.DataInfo['RawData'][-1]]
        Prm.DataInfo['ExpInfo']['05'] = Prm.DataInfo['ExpInfo']['04']


    if ClusterRecs != Clusters.recordings:
        print('Wrong number of recordings! Cannot extract TTLs!')
        RecNo = False
    else:
        RecNo = True

    for rec, Rec in enumerate(Clusters.recordings):
        # if rec < 59: continue
        RawRecExp = [Rec in _ for _ in Recs].index(True)
        RawRecdB = str(Recs[RawRecExp].tolist().index(Rec))
        RawRec = Prm.DataInfo['RawData'][RawRecExp]
        RawRecExp = "{0:02d}".format(RawRecExp)

        RecTTLs = True
        if 'Baseline' in RawRec or 'Basal' in RawRec:
            print('Baseline recordings have no TTLs.')
            RecTTLs = False

        if RecNo and RecTTLs:
            DataFile = Prm.traces['raw_data_files'][rec]

            if 'home/Data/Malfatti' in DataFile or 'home/cerebro/Malfatti' in DataFile:
                DataFile = os.environ['ANALYSISPATH'] + '/' + '/'.join(DataFile.split('/')[5:])

            TTLFile = '/'.join(PrmFile.split('/')[:-1])
            TTLFile += '/' + DataFile.split('/')[-1].split('.')[0]
            if '_Rec' in TTLFile:
                TTLFile += '_TTLs.dat'
            else:
                TTLFile += '_Rec' + "{0:02d}".format(rec)+'_TTLs.dat'

            print(PrmFile, 'rec', rec)
            print('Loading TTLs... ')
            if not glob(TTLFile):
                TTLs = IO.DataLoader(RawRec, Unit='Bits', Recording=RawRecdB)[0]
                ChNo, Proc = IO.OpenEphys.GetChNoAndProcs(RawRec+'/settings.xml')
                TTLs = TTLs[Proc][RawRecdB]

                print('Quantifying... ')
                TTLs = Analysis.QuantifyTTLsPerRec(AnalogTTLs, TTLs[:,TTLCh-1], 1)
                if type(TTLs) == tuple: TTLs = TTLs[0]
                if type(TTLs) != np.ndarray: TTLs = np.array(TTLs)
                print('Saving TTLs to', TTLFile, '...')
                IO.Bin.Write(TTLs, TTLFile)
            else:
                TTLs = IO.Bin.Read(TTLFile)[0]
            print('Done.')

        for I, Id in enumerate(Good):
            Ind = I + (len(Good)*rec)

            # Find the unit in this rec
            SpksId = (Clusters.spike_clusters == Id) & \
                     (Clusters.spike_recordings == Rec)

            if not True in SpksId: continue

            # PSTH
            if RecNo and RecTTLs:
                PSTH = Units.PSTHLine(Clusters.spike_samples[SpksId], TTLs, Rate, PSTHX, Offsets[rec])
                Raster = Units.Raster(Clusters.spike_samples[SpksId], TTLs, Rate, RasterX, Offsets[rec])
            else:
                PSTH, Raster = np.zeros((PSTHX.shape[0], 1)), np.zeros((RasterX.shape[0], 1))*np.nan

            # Waveforms
            Spks = Clusters.all_waveforms[SpksId]
            ChNo = len(Channels)
            RMSs = [(np.nanmean((np.nanmean(Spks[:, :, Ch], axis=0))**2))**0.5
                    for Ch in range(ChNo)]

            # Firing rate
            FiringRate = Units.FiringRate(Clusters.spike_times[SpksId], RecLengths[rec], Offsets[rec]/Rate)

            # ISI
            ISI = Units.ISI(Clusters.spike_times[SpksId], ISISize, Rate)

            # Unit info
            BestCh = RMSs.index(max(RMSs))
            ChSpacing = Prm.DataInfo['Probe']['ChSpacing']
            DV = Prm.DataInfo['ExpInfo'][RawRecExp]['DV']
            if not DV: DV = (Channels[-1]+1)*ChSpacing
            DV = int(DV) - ((ChNo-BestCh+1) * ChSpacing)

            if Prm.DataInfo['ExpInfo'][RawRecExp]['Hz'] != 'Baseline':
                dB = Prm.DataInfo['Audio']['Intensities'][int(RawRecdB)]
                Freq = Prm.DataInfo['ExpInfo'][RawRecExp]['Hz']
                StimType = Prm.DataInfo['ExpInfo'][RawRecExp]['StimType']
                if type(StimType) == list: StimType = '_'.join(StimType)
            else:
                dB, Freq, StimType = 0, '', ''

            UnitRec['UnitId'][Ind] = Id
            UnitRec['DV'][Ind] = DV
            UnitRec['Freq'][Ind] = Freq
            UnitRec['dB'][Ind] = dB
            UnitRec['StimType'][Ind] = StimType
            UnitRec['RMSs'][:, Ind] = RMSs
            UnitRec['PSTHX'][:,Ind] = PSTHX
            UnitRec['RasterX'][:,Ind] = RasterX
            # UnitRec['ISI'][Ind] = ISI
            # UnitRec['PSTH'][Ind] = PSTH
            # UnitRec['Raster'][Ind] = Raster
            # UnitRec['FiringRate'][Ind] = FiringRate
            # UnitRec['Spks'][Ind] = Spks

            if Id != 0:
                Keys = ['ISI', 'PSTH', 'Raster', 'Spks', 'FiringRate']
                for K in Keys:
                    IO.Bin.Write(locals()[K], AnalysisFile + '_' + Exp + '_AllUnits/'+K+'/'+K+'_'+str(Ind)+'.dat')

            del(Spks, PSTH, Raster, ISI, FiringRate)

            # UnitInfo = '_'.join(['Unit'+"{0:04d}".format(Id), StimType,
            #                      str(DV)+'DV', Freq, dB])

            # FigFile = FigPath+'/'+FigPath.split('/')[-1]+'-'+UnitInfo
            # Plot.WF_Raster_PSTH(Spks, Raster, RasterX, PSTH, PSTHX, RMSs, SpksToPlot, Rate, FigFile, Ext, Save, Show)

    # Cleaning
    ValidIds = UnitRec['UnitId'] != 0

    for Key in ['Freq', 'StimType']: UnitRec[Key] = np.array(UnitRec[Key])

    for Key in ['UnitId', 'DV', 'dB', 'Freq', 'StimType']:
        UnitRec[Key] = UnitRec[Key][ValidIds]

    for Key in ['RMSs', 'PSTHX', 'RasterX']:
        UnitRec[Key] = UnitRec[Key][:,ValidIds]

    if Save:
        if UnitRec['UnitId'].size:
            IO.Bin.Write(UnitRec, AnalysisFile + '_' + Exp + '_AllUnits')

    if Return:
        return(UnitRec)
    else:
        del(UnitRec)
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
        UnitRec = Units.UnitRecLoad(AnalysisFolder)

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


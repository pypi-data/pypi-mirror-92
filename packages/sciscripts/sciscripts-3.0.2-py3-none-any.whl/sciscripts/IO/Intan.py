#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20161125
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

import numpy as np
from glob import glob

from sciscripts import Intan_RHA


## Level 0
def Load(File, ChannelMap=[]):
    Data = Intan_RHA.ReadData(File)

    try: len(Data['aux'][0])
    except TypeError: Data['aux'] = Data['aux'].reshape((Data['aux'].shape[0], 1))

    Data = np.hstack((Data['analog'], Data['aux']))

    if ChannelMap:
        ChannelMap = [_-1 for _ in ChannelMap]
        Data[:, (range(len(ChannelMap)))] = Data[:, ChannelMap]

    Rate = 25000

    return(Data, Rate)

# Level 1
def FolderLoad(Folder, ChannelMap=[]):
    Rate = 25000
    Data = {str(F): Load(File, ChannelMap)[0]
            for F,File in enumerate(sorted(glob(Folder+'/*int')))}

    return(Data, Rate)

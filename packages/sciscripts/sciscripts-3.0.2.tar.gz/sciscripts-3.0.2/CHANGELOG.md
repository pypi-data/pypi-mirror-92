# Changelog

## Summary  
- Add `try` statements to make `xdpyinfo` and `xrandr` truly optional;  
- Add option to load binary data as array instead of mmap;  
- Improve anova and t-test output;  
- Start implementing vocalization signal processing.

## Commits  
```
f7c2589 Add automatic plot formatting
8829b53 Adding documentation
327a1c9 Make xdpyinfo and xrandr truly optional
52ed7cb Add AsMMap= argument to Read()
483644c Add Cohen's d for t-test
48e3d73 Add lw= argument to LinePSTH()
99dffad Fix SameScale() errors
5b7003f Implement IsInt() and IsFloat()
843a7e2 Update Slice arguments
6ab908b Fix Tones playback
f38f75a Finish implementing AnOVa
fdb1200 Fix Axes Set and ScatterMean line colors
0361276 Fix Analysis function vs module conflict
1881099 Fix missing import
1d7dca9 Comment unnecessary print
c60add0 Update according to new matplotlib version
9392539 Fix loading different setups
b911c29 Fix LastCommonPath
e7a1aba Add marker argument to Scatter3D
0472e92 Implement .fig loading as dict
9eed20c Fix Scatter3D return ax
6f6a612 Add ScaleBar
8a2669c Add Scatter3D
872a15f Fix Mat.Read()
089d4d8 Add recursive function to clean structs
1fb61e5 Move back to .mat files
5ddfe6c Fix syntax error
00cbefa Fix read/write functions
1d48e81 Change Spectrogram output Fxx and Txx to 1d
296b15e Fix NFFT and implement GetFxx
1e4003b Fix Wav loading Ch dimensions
7caa1a7 Try to implement USVDetect
b26dc36 Make Spectrogram work with 2dArrays
7e7edeb Fix wrong import
83a1b29 Implement reading of MouseProfilerTracker XML files
3b61196 Implement lower-level returning of Tree and Root
534d6a3 Replace .mat by .dat
9d050ca Implement "Get coordinate by mouse click"
dfff54e Start implementing Vocalizations analysis
2c9e537 Implement Peaks colors
a800e87 Removing GetDuplicates
cd6f9f2 Trying to implement GetDuplicates
c73d3d4 fix missing :
d557e4a Implement WhereMultiple
354f5fc Implement conversion from Kwik to Bin
13b278e Implement distance and area calculations
4a3749f Implement animation plot
c49d8e6 Implement entropy calculations
```

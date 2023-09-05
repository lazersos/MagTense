# For intel
#LINK = /apps/external/intel/2019/compilers_and_libraries_2019.4.243/linux/bin/intel64/xiar rc
#FC = /apps/external/intel/2019/compilers_and_libraries_2019.4.243/linux/bin/intel64/ifort
#FFLAGS ?= -r8 -O3 -fpp -fpe0 -fp-model source -fpic -libs:static

# For GNU Compilers
LINK = ar -cruv 
FC = /opt/local/bin/gfortran
FFLAGS = -cpp -O3 -fopenmp -fdefault-real-8 -fdefault-double-8  -ffixed-line-length-none -ffree-line-length-none -fPIC -fallow-argument-mismatch

# Matlab (system dependent)
MATLABROOT = /Applications/MATLAB_R2022b.app

# These are convient helpers (should probably not be changed)
NumIntLib = ../../NumericalIntegration/NumericalIntegration/
TileDemagTensorLib = ../../TileDemagTensor/TileDemagTensor/
DemagFieldLib = ../../DemagField/DemagField/
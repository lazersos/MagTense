
include ../../../make.inc

FFLAGS += -I$(NumIntLib) -I$(TileDemagTensorLib) -I$(MATLABROOT)/extern/include

.KEEP_STATE:
.SUFFIXES:
.SUFFIXES: .for .f90 .F90 .f .o
.f.o:
	$(FC) -c $(FFLAGS) $<
.f90.o:
	$(FC) -c $(FFLAGS) $<
.F90.o:
	$(FC) -c $(FFLAGS) $<
.for.o:
	$(FC) -c $(FFLAGS) $<

DemagFieldLib = $(FC) DemagFieldGetSolution.o MagParameters.o MagTileIO.o spline.o IterateMagnetSolution.o

libDemagField.a: $(DemagFieldLib)
	$(LINK) libDemagField.a DemagFieldGetSolution.o MagParameters.o MagTileIO.o  spline.o IterateMagnetSolution.o


clean:
	rm -f *.o *.x *.mod *.a


DemagFieldGetSolution.o	:DemagFieldGetSolution.f90
MagParameters.o	:MagParameters.f90
MagTileIO.o	:MagTileIO.f90
spline.o	:spline.f90
IterateMagnetSolution.o	:IterateMagnetSolution.f90 MagParameters.o DemagFieldGetSolution.o spline.o MagTileIO.o





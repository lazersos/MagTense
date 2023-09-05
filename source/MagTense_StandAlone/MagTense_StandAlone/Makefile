
include ../../../make.inc

NumIntLib = ../../NumericalIntegration/NumericalIntegration/
TileDemagTensorLib = ../../TileDemagTensor/TileDemagTensor/
DemagFieldLib = ../../DemagField/DemagField/

LIB_NumIntLib = $(NumIntLib)libNumericalIntegration.a
LIB_TileDemagTensorLib = $(TileDemagTensorLib)libTileDemagTensor.a
LIB_DemagFieldLib = $(DemagFieldLib)libDemagField.a

FFLAGS += -I$(NumIntLib) -I$(TileDemagTensorLib) -I$(DemagFieldLib)

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

MagTense.x = StandAloneIO.o MagTense_StandAlone.o

MagTense.x: $(MagTense.x)
	$(FC) -o MagTense.x $(MagTense.x) $(LIB_NumIntLib) $(LIB_DemagFieldLib) $(LIB_TileDemagTensorLib) $(LIB_DemagFieldLib) $(FFLAGS)

#
#
#


clean:
	rm -f *.o *.x *.mod *.a


IO.o	:IO.f90
MagTense_StandAlone.o		:MagTense_StandAlone.f90 StandAloneIO.o






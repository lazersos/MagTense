
include ../../../make.inc

NumIntLib = ../../NumericalIntegration/NumericalIntegration/
TileDemagTensorLib = ../../TileDemagTensor/TileDemagTensor/
DemagFieldLib = ../../DemagField/DemagField/

FFLAGS += -I$(NumIntLib) -I$(TileDemagTensorLib) -I$(DemagFieldLib) -I$(MATLABROOT)/extern/include

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

MagneticForceIntegratorLib = $(FC) MagForceIO.o MagForceMaxwellStressTensor.o MagneticForce.o

libMagneticForceIntegrator.a: $(MagneticForceIntegratorLib)
	$(LINK) libMagneticForceIntegrator.a MagForceIO.o MagForceMaxwellStressTensor.o MagneticForce.o


clean:
	rm -f *.o *.x *.mod *.a


MagForceIO.o	:MagForceIO.f90
MagForceMaxwellStressTensor.o	:MagForceMaxwellStressTensor.f90 
MagneticForce.o	:MagneticForce.f90

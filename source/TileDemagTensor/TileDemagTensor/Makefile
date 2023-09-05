
include ../../../make.inc

FFLAGS += -I$(NumIntLib)

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

TileDemagTensorLib = $(FC) TileTensorHelperFunctions.o TileTriangle.o TileCircPieceTensor.o TileCylPieceTensor.o TileRectangularPrismTensor.o TilePlanarCoilTensor.o  TileNComponents.o

libTileDemagTensor.a: $(TileDemagTensorLib)
	$(LINK) libTileDemagTensor.a TileTensorHelperFunctions.o TileTriangle.o TileCircPieceTensor.o TileCylPieceTensor.o TileRectangularPrismTensor.o TilePlanarCoilTensor.o  TileNComponents.o


clean:
	rm -f *.o *.x *.mod *.a

#SpecialFunctions.o	:SpecialFunctions.f90
TileTensorHelperFunctions.o	:TileTensorHelperFunctions.f90
TileCircPieceTensor.o	:TileCircPieceTensor.f90 TileTensorHelperFunctions.o
TileCylPieceTensor.o   :TileCylPieceTensor.f90 TileTensorHelperFunctions.o
TileRectangularPrismTensor.o   :TileRectangularPrismTensor.f90 TileTensorHelperFunctions.o
TilePlanarCoilTensor.o   :TilePlanarCoilTensor.f90 TileTensorHelperFunctions.o
TileTriangle.o   :TileTriangle.f90 TileTensorHelperFunctions.o
TileNComponents.o	:TileNComponents.f90 TileTensorHelperFunctions.o TileTriangle.o TileCircPieceTensor.o TileCylPieceTensor.o TileRectangularPrismTensor.o TilePlanarCoilTensor.o





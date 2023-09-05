
include ../../../make.inc

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

NumericalIntegrationLib = $(FC) IntegrationDataTypes.o quadpack.o NumericalIntegrals.o ODE_Solvers.o ODE_MagTense.o RKSuitef90.o util.o locate.o IOgeneral.o

libNumericalIntegration.a: $(NumericalIntegrationLib)
	$(LINK) libNumericalIntegration.a IntegrationDataTypes.o quadpack.o NumericalIntegrals.o ODE_Solvers.o ODE_MagTense.o RKSuitef90.o util.o locate.o IOgeneral.o SpecialFunctions.o


clean:
	rm -f *.o *.x *.mod *.a


quadpack.o	:quadpack.f90 IntegrationDataTypes.o
IntegrationDataTypes.o	:IntegrationDataTypes.f90 
NumericalIntegrals.o	:NumericalIntegrals.f90 quadpack.o IntegrationDataTypes.o
RKSuitef90.o	:RKSuitef90.f90
ODE_Solvers.o	:ODE_Solvers.f90 RKSuitef90.o SpecialFunctions.o
util.o	:util.f90
locate.o :locate.for

import numpy as np

from typing import Optional, List
from magtense.lib import magtensesource


class MicromagProblem:
    '''
    Micromagnetic problem using the Fortran implementation of MagTense.

    Args:
        res: Resolution of grid.
        grid_L: Spatial extensions.
        grid_nnod:
        grid_type: Curently only 'uniform' is supported.
        prob_mode:
        solver:
        A0: Anisotropy constant.
        Ms: Saturation magnetization [A/m].
        K0: Exchange constant.
        alpha: Dampening constant.
        gamma: Gyromagnetic factor.
        max_T0:
        nt_conv:
        conv_tol: The convergence tolerence, which is the maximum change in 
                  magnetization between two timesteps.
        tol: Relative tolerance for the Fortran ODE solver.
        thres: Fortran ODE solver, when a solution component Y(L) is less in
               magnitude than thres_value its set to zero.
        setTimeDis:
        dem_thres: Initial value of the demag threshold is zero, i.e. it is not used.
        demag_approx:
        exch_nval: Number of values in the exchange operator matrix.
        exch_nrow: Number of rows in the exchange operator matrix.
        filename:
        cuda: Optional GPU support via CUDA.
        cvode:
        precision: Precision for the demag tensor. Only SP is supported.
        n_threads: Number of threads used by OpenMP for building the demag tensor.
        N_ave:
        t_alpha:
        alpha_fct:
    '''
    def __init__(self,
        res: List[int],
        grid_L: List[int] = [500e-9, 125e-9, 3e-9],
        grid_nnod: int = 0,
        grid_type: Optional[str] = 'uniform',
        prob_mode: Optional[str] = 'new',
        solver: Optional[str] = 'dynamic',
        A0: float = 1.3e-11,
        Ms: float = 8e5,
        K0: float = 0.,        
        alpha: float = 0.02,
        gamma: float = 0.,
        max_T0: float = 2.,
        nt_conv: int = 1,
        conv_tol: float = 1e-4,
        tol: float = 1e-4,
        thres: float = 1e-6,
        setTimeDis: int = 10,
        dem_thres: float = 0.,
        demag_approx: Optional[str] = None,
        exch_nval: int = 1,
        exch_nrow: int = 1,
        filename: str = 't',
        cuda: bool = False,
        cvode: bool = False,
        precision: bool = False,
        n_threads: int = 1,
        N_ave: List[int] = [1, 1, 1],
        t_alpha: np.array = np.zeros(1),
        alpha_fct = lambda t: np.atleast_2d(t).T * 0
    ) -> None:
        ntot = np.prod(res)
        self.ntot = ntot
        self.grid_nnod = grid_nnod
        self.nt_conv = nt_conv
        self.exch_nval = exch_nval
        self.exch_nrow = exch_nrow
        
        self.grid_n = np.array(res, dtype=np.int32, order='F')
        self.grid_L = np.array(grid_L, dtype=np.float64, order='F')
        self.grid_pts = np.zeros(shape=(ntot,3), dtype=np.float64, order='F')
        self.grid_ele = np.zeros(shape=(4,ntot), dtype=np.float64, order='F')
        self.grid_nod = np.zeros(shape=(grid_nnod,3), dtype=np.float64, order='F')
        self.grid_abc = np.zeros(shape=(ntot,3), dtype=np.float64, order='F')
        self.u_ea = np.zeros(shape=(ntot, 3), dtype=np.float64, order='F')
        
        self.set_mm_grid_type(grid_type)
        self.set_mm_prob_mode(prob_mode)
        self.set_mm_solver(solver)
        
        self.A0 = A0
        self.Ms = Ms
        self.K0 = K0
        self.alpha = alpha
        self.gamma = gamma
        self.max_T0 = max_T0
       
        self.t_conv = np.zeros(shape=(nt_conv), dtype=np.float64, order='F')
        self.conv_tol = np.array(np.repeat(conv_tol, nt_conv), dtype=np.float64, order='F')
        self.tol = tol
        self.thres = thres
        self.setTimeDis = setTimeDis

        self.m0 = np.zeros(shape=(ntot,3), dtype=np.float64, order='F')
        theta = np.pi * np.random.rand(ntot)
        phi = 2 * np.pi * np.random.rand(ntot)
        self.m0[:,0] = np.sin(theta) * np.cos(phi)
        self.m0[:,1] = np.sin(theta) * np.sin(phi)
        self.m0[:,2] = np.cos(theta)

        self.dem_thres = dem_thres
        self.set_mm_demag_approx(demag_approx)

        self.nt_alpha = len(t_alpha)
        self.alphat = np.zeros(shape=(self.nt_alpha,2), dtype=np.float64, order='F')
        self.alphat[:,0] = t_alpha
        self.alphat[:,1] = alpha_fct(t_alpha)

        self.exch_val = np.zeros(shape=(exch_nval), dtype=np.int32, order='F')
        self.exch_rows = np.zeros(shape=(exch_nrow), dtype=np.int32, order='F')
        self.exch_rowe = np.zeros(shape=(exch_nrow), dtype=np.int32, order='F')
        self.exch_col = np.zeros(shape=(exch_nval), dtype=np.int32, order='F')

        self.N_load = len(filename)
        self.N_file_in = filename
        self.N_ret = len(filename)
        self.N_file_out = filename

        self.cuda = int(cuda)
        self.cvode = int(cvode)
        self.precision = int(precision)
        self.n_threads = n_threads
        self.N_ave = np.array(N_ave, dtype=np.int32, order='F')

    def set_mm_demag_approx(self, nm=None):
        approx_dict = {None: 1, 'threshold': 2, 'fft_thres': 3,
                      'threshold_fraction': 4, 'fft_threshold_fraction': 5}
        self.dem_appr = approx_dict[nm]

    def set_mm_grid_type(self, nm=None):
        grid_dict = {None: -1, 'uniform': 1, 'tetrahedron': 2, 'unstructuredPrisms': 3}
        self.grid_type = grid_dict[nm]

    def set_mm_prob_mode(self, nm=None):
        mode_dict = {None: -1, 'new': 1, 'old': 2}
        self.prob_mode = mode_dict[nm]

    def set_mm_solver(self, nm=None):
        solver_dict = {None: -1, 'explicit': 1, 'dynamic': 2, 'implicit': 3}
        self.solver = solver_dict[nm]


    def run_simulation(self, t_end, nt, fct_Hext, nt_Hext):
        t = np.linspace(0, t_end, nt)
        # Calculating applied field as a function of time
        Hext = np.zeros(shape=(nt_Hext, 4), dtype=np.float64, order='F')
        Hext[:,0] = np.linspace(0, t_end, nt_Hext)
        Hext[:,1:4] = fct_Hext(np.linspace(0, t_end, nt_Hext))

        return magtensesource.fortrantopythonio.runmicromagsimulation( 
            ntot=self.ntot,
            grid_n=self.grid_n,
            grid_l=self.grid_L,
            grid_type=self.grid_type,
            u_ea=self.u_ea,
            problemmode=self.prob_mode,
            solver=self.solver,
            a0=self.A0,
            ms=self.Ms,
            k0=self.K0,
            gamma=self.gamma,
            alpha=self.alpha,
            maxt0=self.max_T0,
            nt_hext=nt_Hext,
            hext=Hext,
            nt=nt,
            t=t,
            m0=np.concatenate((self.m0[:,0], self.m0[:,1], self.m0[:,2]), axis=None),
            dem_thres=self.dem_thres,
            usecuda=self.cuda,
            dem_appr=self.dem_appr,
            n_ret=self.N_ret,
            n_file_out=self.N_file_out,
            n_load=self.N_load,
            n_file_in=self.N_file_in,
            settimedis=self.setTimeDis,
            nt_alpha=self.nt_alpha,
            alphat=self.alphat,
            tol=self.tol,
            thres=self.thres,
            usecvode=self.cvode,
            nt_conv=self.nt_conv,
            t_conv=self.t_conv,
            conv_tol=self.conv_tol,
            grid_pts=self.grid_pts,
            grid_ele=self.grid_ele,
            grid_nod=self.grid_nod,
            grid_nnod=self.grid_nnod,
            exch_nval=self.exch_nval,
            exch_nrow=self.exch_nrow,
            exch_val=self.exch_val,
            exch_rows=self.exch_rows,
            exch_rowe=self.exch_rowe,
            exch_col=self.exch_col,
            grid_abc=self.grid_abc,
            useprecision=self.precision,
            nthreadsmatlab=self.n_threads,
            n_ave=self.N_ave
        )

import os
import sys
import numpy as np
import math
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../source')
import MagTense
import MagTenseStandalone
import util_plot
import util_eval

def main():
    # Define validation tile
    tile_val = MagTense.Tiles(1)
    tile_val.set_center_pos([[0.45, math.pi/3, 0.35]])
    tile_val.set_dev_center([0.5, math.pi/7, 0.15])
    tile_val.set_offset_i([0.1, 0.3, 0.2],0)
    tile_val.set_rotation_i([0, 0, 0],0)
    tile_val.set_tile_type(3)
    tile_val.set_remanence(1.2 / (4*math.pi*1e-7))
    tile_val.set_easy_axis([[-0.3095974 , -0.22493568,  0.92387953]])
    tile_val.set_color([[1, 0, 0]])

    eval_offset = [0.406328622087633, 0.8631363102808783, 0.55] 

    # Load reference points from COMSOL calculation
    COMSOL_eval_path = os.path.dirname(os.path.abspath(__file__)) + '/../../documentation/examples_FEM_validation/Validation_circpiece/'

    (eval_points_x, H_norm_x_COMSOL) = util_eval.load_COMSOL_eval('Validation_circpiece_normH_x.txt', eval_offset, COMSOL_eval_path)
    (eval_points_y, H_norm_y_COMSOL) = util_eval.load_COMSOL_eval('Validation_circpiece_normH_y.txt', eval_offset, COMSOL_eval_path)
    (eval_points_z, H_norm_z_COMSOL) = util_eval.load_COMSOL_eval('Validation_circpiece_normH_z.txt', eval_offset, COMSOL_eval_path)

    # x-axis
    (updated_tiles_x, H_x) = MagTense.run_simulation(tile_val, eval_points_x)
    H_norm_x_MagTense  = MagTense.get_norm_magnetic_flux(H_x)
    
    # y-axis
    (updated_tiles_y, H_y) = MagTense.run_simulation(tile_val, eval_points_y)
    H_norm_y_MagTense  = MagTense.get_norm_magnetic_flux(H_y)

    # z-axis
    (updated_tiles_z, H_z) = MagTense.run_simulation(tile_val, eval_points_z)
    H_norm_z_MagTense  = MagTense.get_norm_magnetic_flux(H_z)
    
    fig, ax = plt.subplots(1,3)
    fig.suptitle("CIRCPIECE - MagTensePython vs. COMSOL")
    util_eval.add_subplot(ax[0], eval_points_x[:,0], 'x_axis', H_norm_x_MagTense, H_norm_x_COMSOL)
    util_eval.add_subplot(ax[1], eval_points_y[:,1], 'y_axis', H_norm_y_MagTense, H_norm_y_COMSOL)
    util_eval.add_subplot(ax[2], eval_points_z[:,2], 'z_axis', H_norm_z_MagTense, H_norm_z_COMSOL)
    plt.show()

main()

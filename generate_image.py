import numpy as np
import matplotlib.pyplot as plt
from convert_image_to_array import convertImageToGSLIBFile, convertImageToHardData
import mpslib as mps
from pre_process_data import ContrastStretching
import skimage.io


class GenerateImage():
    def __init__(self):
        # # Choose to compute entropy
        # self.mpslib.par['do_entropy'] = 1
        self.image = []
        self.time = []
    
    def convert_histogram(self, images):
        self.images = images
        for index, i in enumerate(self.images):
            new_image = ContrastStretching(i, str(index + 1) + '_scale')
            new_image_with_3_channels = new_image.add_channels()
            new_image_percentile_stretching = new_image.quantile_transform(new_image_with_3_channels)
            new_image.save_image(new_image_percentile_stretching)

    def create_TI_file(self):
        self.ti = './imgs/imgs_converted/2_scale.tif'
        self.dat_ti = convertImageToGSLIBFile(self.ti)
        self.original_ti = mps.eas.read('ti.dat')
        
    def configure_MPS_method(self, fig_size, second_scale_resolution):
        # Initialize MPSlib using mps_genesim algorithm, and seetings
        self.first_scale = './imgs/imgs_converted/1_scale.tif'
        self.mpslib = mps.mpslib(method='mps_snesim_tree')
        self.mpslib.par['simulation_grid_size']=np.array([fig_size*8.92, fig_size*8.92, 8.92])
        self.mpslib.par['grid_cell_size']=np.array([second_scale_resolution, second_scale_resolution, second_scale_resolution])
        self.ncond = np.array([i for i in range(0, 20, 10)])
        self.mpslib.par['n_real'] = 3
        self.mpslib.par['ti_fnam'] = './ti.dat'
        self.mpslib.par['n_threads'] = 4
        self.mpslib.par["n_multiple_grids"] = 2
        self.mpslib.d_hard = convertImageToHardData(self.first_scale)
        self.mpslib.par['out_folder'] = '.'
        return self.mpslib
    
    def save_figure(self, index_fig):
        fig1 = plt.figure(figsize=(5, 5))
        plt.imshow(np.transpose(np.squeeze(self.original_ti['Dmat'])))
        plt.imsave('./results_fig/original.png', np.transpose(np.squeeze(self.original_ti['Dmat'])), cmap="gray")
        plt.close(fig1)
        for index, ncond in enumerate(self.ncond):
            fig = plt.figure(figsize=(5, 5))
            plt.title('CPU time = %.1f' % (self.time[index]) + 's')
            images_length = len(np.transpose(np.squeeze(self.image[index])))
            for i in range(images_length):
                skimage.io.imsave('./results_fig/' + 'Figure_ncond_' + str(ncond) + f'_{i:03}' + '.tif', np.transpose(np.squeeze(self.image[index]))[i], cmap='gray')
            np.transpose(np.squeeze(self.image[index])).save('./results_fig/' + 'Figure_' + str(index_fig) + '_ncond_' + str(ncond) +  '.tiff', format="TIFF", save_all=True)
            plt.close(fig)

    def generate_time_figure(self, index):
        fig2 = plt.figure(figsize=(5, 5))
        plt.plot(self.ncond,self.time,'.')
        plt.grid()
        plt.xlabel('n_cond')
        plt.ylabel('simulation time (s)')
        fig2.savefig('./results_fig/' + 'Figure_' + str(index) + '_ncond_time' + '.png')
        plt.close(fig2)


    def run(self):
        for ncond in self.ncond:
            self.mpslib.par['n_cond'] = ncond
            self.mpslib.run_parallel()
            self.image.append(self.mpslib.sim[-1])
            self.time.append(self.mpslib.time)
        return

if __name__ == "__main__":
    image = GenerateImage()
    image.convert_histogram()
    image.create_TI_file()
    image.configure_MPS_method()
    image.run()
    image.save_figure()
    image.generate_time_figure()

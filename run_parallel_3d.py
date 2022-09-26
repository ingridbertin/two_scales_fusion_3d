import glob
import numpy as np
from PIL import Image
from generate_image import GenerateImage

class Fusion():
    def __init__(self):
        self.images_first_scale = glob.glob(r"./imgs/imgs_scale1_50_50_50/*")
        self.images_second_scale = glob.glob(r"./imgs/imgs_scale2_100_100_50/*")
        print(self.images_second_scale)
        
    def run_3d(self):
        # for each slice does the MPS to merge the fine and coarse scale data
        # xy plane
        for index, image in enumerate(self.images_first_scale):
            generate_image = GenerateImage()
            img =  Image.open(image, "r")
            numpyData = np.asarray(img)
            first_scale_Nx = numpyData.shape[0]
            self.images = [image, self.images_second_scale[index]]
            generate_image.convert_histogram(self.images)
            generate_image.create_TI_file()
            
            generate_image.configure_MPS_method(first_scale_Nx, 3.771*10**(-6))
            generate_image.run()
            generate_image.save_figure(index)
            generate_image.generate_time_figure(index)    

if __name__ == "__main__":
    fusion = Fusion()
    fusion.run_3d()
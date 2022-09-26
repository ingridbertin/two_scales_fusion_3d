import glob
import numpy as np
import skimage.io


class Porosity_Estimation():
    def __init__(self):
        self.images = glob.glob('./binary_images/ncon50/binary_' + '[0-9]'+ '[0-9]' + '_ncond50.*')
        self.porosity = 0
        self.zero_values = 0
        self.one_values = 0
        self.slices = []
    
    def load_image(self):
            # load the image
        for img in self.images:
            self.slices.append(skimage.io.imread(img, as_gray=True))
        return
    
    def main(self):
        for image in self.slices:
            self.zero_values += np.unique(image, return_counts=True)[1][0]
            self.one_values += np.unique(image, return_counts=True)[1][1]

        self.porosity = self.zero_values/(self.zero_values + self.one_values)
        print(self.porosity)
        return self.porosity

if __name__ == "__main__":
    porosity = Porosity_Estimation()
    porosity.load_image()
    porosity.main()
    
    
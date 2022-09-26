import glob
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
from skimage.filters import threshold_otsu

class Image_segmentation():
    def __init__(self):
        # # Choose to compute entropy
        # self.mpslib.par['do_entropy'] = 1
        self.images = glob.glob('./results_fig/Figure_' + '[0-9][0-9]' + '_ncond_50.*')
        self.binary_mask = []
        self.slices = []

    def load_image(self):
        # load the image
        for img in self.images:
            image_rgba = skimage.io.imread(img, as_gray=True)
            self.slices.append(image_rgba) 
        return
    
    def convert_image_and_compute_threshold(self):
        # convert the image to grayscale and compute automatic thresholding
        self.t = threshold_otsu(self.slices[0])
        print("Found automatic threshold t = {}.".format(self.t))
        return
    
    def segment_image(self):
        for img in self.slices:        
            # create a binary mask with the threshold found by Otsu's method
            self.binary_mask.append(img > self.t)
        return self.binary_mask
    
    def save_binary_images(self):
        # save the binary images in the folder
        for i, image in enumerate(self.binary_mask):
            fig = plt.figure(figsize=(12, 12))
            ax = fig.add_subplot(2,2,1)
            if i<10:
                plt.imsave('./binary_images/ncon50/binary_0' + str(i) + '_ncond50' + '_' + str(j) + '.png', image, cmap="gray")
            else:
                plt.imsave('./binary_images/ncon50/binary_' + str(i) + '_ncond50' + '_' + str(j) + '.png', image, cmap="gray")
            plt.close(fig)

if __name__ == "__main__":
    image = Image_segmentation()
    image.load_image()
    image.convert_image_and_compute_threshold()
    image.segment_image()
    image.save_binary_images()
